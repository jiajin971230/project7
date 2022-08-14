# -*- codeing = uft-8 -*-*
# @Time : 2022/5/14 22:28
# @Author : 曾佳进
# @File : pymysql_pool.py
# @Software : PyCharm
import pymysql
import warnings
import queue
import logging
import threading
import pymysql.cursors
warnings.filterwarnings('error',category=pymysql.err.Warning)
#use logging module for easy debug
logging.basicConfig(format='%(asctime)s %(levelname)8s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logger=logging.getLogger(__name__)
logger.setLevel('WARNING')

class Connection(pymysql.connections.Connection):
    _pool=None
    _reusable_expection=(pymysql.err.ProgrammingError,pymysql.err.IntegrityError,pymysql.err.NotSupportedError,pymysql.err.DatabaseError )

    def __init__(self,*args,**kwargs):
        pymysql.connections.Connection.__init__(self,*args,**kwargs)
        self.args=args
        self.kwargs=kwargs

    def __exit__(self, exc,value,trackback):
        pymysql.connections.Connection.__exit__(self,exc,value,trackback)
        if self._pool:
            if not exc or exc in self._reusable_expection:
                #reusable connection
                self._pool.put_connection(self)
            else:
                #no reusable connection,close it and create a new one then put in to pool
                self._pool.put_connection(self._recreata(*self.args,**self.kwargs))
                self._pool=None
                try:
                    self.close()
                    logger.warning('Close not reusable connection from pool({}) caused by {}'.format(self._pool,self._reusable_expection))
                except Exception:
                    pass
    def _recreata(self,*args,**kwargs):
        conn=Connection(*args,**kwargs)
        logger.debug('Create new connection due to pool({}) lacking'.format(self._pool.name))
        return conn

    def close(self):
        '''
        Overwrite the close() method of pymysql.connections.Connection
        with pool,put connection back to pool;
        without pool,send the quit message and close the socket
        '''
        if self._pool:
            self._pool.put_connection(self)
        else:
            pymysql.connections.Connection.close(self)

    def execute_query(self,query,args=(),dictcursor=True,return_one=False,exec_many=False):
        '''
        A wrapped method of pymysql's execute() or executrmany().
        dictcursor: whether want use the dict cursor(cursor's default type is tuple)
        return_one: whether want onle one row of the result
        exec_many: whether use pymysql's executemany() method
        '''
        with self:
            cur=self.cursor() if not dictcursor else self.cursor(pymysql.cursors.DictCursor)
            try:
                if exec_many:
                    cur.executemany(query,args)
                else:
                    cur.execute(query,args)
            except Exception:
                raise
            #if no record match the query,return one==False,else return None
            return cur.fetchone() if return_one else cur.fetchall()

    def execute(self,sql,args=(),dictcursor=True):
        '''
        insert,update,delete
        dictcursor:whether want use the dict cursor(cursor's default type is tuple)
        '''
        with self:
            cur=self.cursor if not dictcursor else self.cursor(pymysql.cursors.DictCursor)
            try:
                result=cur.execute(sql,args)
                self.commit();
            except Exception:
                raise
            return result

class ConnectionPool:
    '''
    return connection_pool object ,which has method can get connection from a pool with timeout
    '''
    _HARD_LIMIT=100
    _THREAD_LOCAL=threading.local()
    _THREAD_LOCAL.retry_counter=0

    def __init__(self,size=5,name=None,*args,**kwargs):
        self._pool=queue.Queue(self._HARD_LIMIT)
        self.name=name if name else '-'.join(
            [kwargs.get('host','localhost'),str(kwargs.get('port',3306)),str(kwargs.get('user','')),kwargs.get('database','')])
        for _ in range(size if size < self._HARD_LIMIT else self._HARD_LIMIT ):
            conn=Connection(*args,**kwargs)
            conn._pool=self
            self._pool.put(conn)
    def get_connection(self,timeout=1,retry_num=1):
        '''
        timeout:timeout of get a connection from pool ,should be a int(0 means return or raise immediately)
        retry_num:how many times will retry to get a connection
        '''
        try:
            conn=self._pool.get(timeout=timeout) if timeout>0 else self._pool.get_nowait()
            logger.debug('Get connection from pool({})'.format(self.name))
            return conn
        except queue.Empty:
            if retry_num>0:
                self._THREAD_LOCAL.retry_counter+=1
                logger.debug('Rrtry get connection from pool({}),the {} times'.format(self.name,self._THREAD_LOCAL))
                retry_num-=1
                return self.get_connection(timeout,retry_num)
            else:
                total_times=self._THREAD_LOCAL.retry_counter+1
                self._THREAD_LOCAL.retry_counter=0
                raise GetConnectionFromPoolError("can't get connection from pool({}) within {}*{} second(s)"
                                                 .format(self.name,timeout,total_times))
    def put_connection(self,conn):
        if not conn._pool:
            conn._pool=self
        conn.cursor().close()
        try:
            self._pool.put_nowait(conn)
            logger.debug('put connection back to pool({})'.format(self.name))
        except queue.Full:
            logger.warning('put connection to pool({}) error,pool if full,siae:{}'.format(self.name,self.size))
    def size(self):
        return self._pool.qsize()

class GetConnectionFromPoolError(Exception):
    '''
    Exception related can't get commection from pool which timeout second
    '''