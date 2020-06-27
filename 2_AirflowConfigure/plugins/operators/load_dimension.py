from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    
    
    @apply_defaults
    def __init__(self,
                 redshift_conn_id="",
                 target_table="",
                 mode = "",
                 insert_table_sql = "",
                 create_table_sql = "",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.target_table = target_table
        self.mode = mode
        self.insert_table_sql = insert_table_sql
        self.create_table_sql = create_table_sql
        
    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        self.log.info('Creating the respective dimension table in redshift before insert')
        redshift.run(format(self.create_table_sql))
        
        
        self.log.info(f"Loading dimension table {self.table} in Redshift")
        
        if self.mode == 'append':
            insert_sql = f"INSERT INTO {self.table} {self.insert_table_sql}"
        
        else:
            insert_sql = f"DELETE FROM {self.target_table}; INSERT INTO {self.target_Table} {self.insert_table_sql}"
            
        self.log.info("Command is " + insert_sql)    
        redshift.run(insert_sql)
