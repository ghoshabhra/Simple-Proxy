import logging

logging.basicConfig(filename="simple_proxy.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

def getLogger():
    """
    Get a :class: `logging.getLogger` object

    :return: logging oject
    :rtype: :class:`logging.getLogger`
    """
    return logging.getLogger()


