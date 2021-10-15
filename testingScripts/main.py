import lithops
from lithops.multiprocessing import Pool


iterdata = ['Gil', 'Dana', 'John', 'Scott']


def add_value(name):
    return 'Hello ' + name


def execute_lithops_function():
    lt = lithops.FunctionExecutor()
    lt.map(add_value, iterdata)
    print(lt.get_result())
    lt.clean()


def double(i):
    return i * 2


def execute_lithops_multi():
    with Pool() as pool:
        result = pool.map(double, [1, 2, 3, 4, 5])
        print(result)


def put_object():
    storage = lithops.Storage()
    storage.put_object(bucket='cos-lithops-thesis-bucket',
                       key='test.txt',
                       body='Hello World')

    print(storage.get_object(bucket='cos-lithops-thesis-bucket',
                             key='test.txt'))


if __name__ == '__main__':
    execute_lithops_multi()