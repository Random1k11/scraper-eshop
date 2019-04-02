from sqlalchemy.orm import sessionmaker
from unident.models import db_connect, create_table, Product, HistoryProduct, check_existence_row_in_db,\
                                get_price_from_databse, insert_row_to_history_database, update_price
from sqlalchemy.exc import IntegrityError

import logging

logger = logging.getLogger('pipeline')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s, level: %(levelname)s, file: %(name)s, function: %(funcName)s], message: %(message)s')
file_handler = logging.FileHandler('unident/logs/pipeline.log', mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
logger.addHandler(file_handler)


class UnidentSpiderPipeline(object):

    def __init__(self):

        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        session = self.Session()
        productDB = Product()
        productDB.Title        = item["Title"]
        productDB.Price        = item["Price"]
        productDB.Brand        = item["Brand"]
        productDB.CodeProduct  = item["CodeProduct"]
        productDB.CodeProducer = item["CodeProducer"]
        productDB.Description  = item["Description"]

        try:
            if check_existence_row_in_db(productDB.CodeProduct) == None:
                logger.debug('=== Записываю в БД новый товар ===')
                session.add(productDB)
                session.commit()
            else:
                if int(productDB.Price) != int(get_price_from_databse(productDB.CodeProduct)):
                    logger.info('=== Цена товара изменилась ===')
                    try:
                        insert_row_to_history_database(productDB.CodeProduct)
                        logger.info('=== Записываю в таблицу с историей ===')
                    except IntegrityError:
                        pass
                    update_price(productDB.CodeProduct, productDB.Price)
                    logger.info('=== Цена товара обновлена ===')

        except:
            session.rollback()
            raise
        finally:
            session.close()
