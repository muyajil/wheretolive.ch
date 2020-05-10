import logging
import os

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable

logging.basicConfig(level=os.environ.get("LOGLEVEL"))


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return (
        compiler.visit_drop_table(element).replace("DROP TABLE", "DROP TABLE IF EXISTS")
        + " CASCADE"
    )
