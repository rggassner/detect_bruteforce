from elasticsearch import Elasticsearch
from config import (
    ELASTICSEARCH_HOST, ELASTICSEARCH_PORT, ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD,
    ELASTICSEARCH_CA_CERT_PATH, ELASTICSEARCH_TIMEOUT, ELASTICSEARCH_RETRY, ELASTICSEARCH_RETRIES,
    ELASTICSEARCH_HTTP_COMPRESS, ELASTICSEARCH_VERIFY_CERTS, ELASTICSEARCH_COMPAT_VERSION
)

class DatabaseConnection:
    """
    A wrapper class for managing an Elasticsearch connection using the official Elasticsearch client.
    Adds API compatibility headers and scroll cleanup.
    """
    def __init__(self):
        es_config = {
            "hosts": [f"https://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"],
            "basic_auth": (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD),
            "verify_certs": ELASTICSEARCH_VERIFY_CERTS,
            "request_timeout": ELASTICSEARCH_TIMEOUT,
            "retry_on_timeout": ELASTICSEARCH_RETRY,
            "max_retries": ELASTICSEARCH_RETRIES,
            "http_compress": ELASTICSEARCH_HTTP_COMPRESS,
            "ssl_show_warn": False,
            "headers": {
                # Force API compatibility with your ES cluster
                "Accept": f"application/vnd.elasticsearch+json; compatible-with={ELASTICSEARCH_COMPAT_VERSION}",
                "Content-Type": f"application/vnd.elasticsearch+json; compatible-with={ELASTICSEARCH_COMPAT_VERSION}"
            }
        }

        if ELASTICSEARCH_CA_CERT_PATH:
            es_config["ca_certs"] = ELASTICSEARCH_CA_CERT_PATH

        self.es = Elasticsearch(**es_config)
        self.con = self.es

    def commit(self):
        pass

    def close(self):
        self.es.close()

    def search(self, *args, **kwargs):
        return self.es.search(*args, **kwargs)

    def scroll(self, *args, **kwargs):
        return self.es.scroll(*args, **kwargs)

    def clear_scroll(self, *args, **kwargs):
        """Clear scroll context in Elasticsearch to free memory."""
        return self.es.clear_scroll(*args, **kwargs)
