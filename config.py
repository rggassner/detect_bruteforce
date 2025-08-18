# ===== ELASTICSEARCH CONNECTION =====
ELASTICSEARCH_HOST = '127.0.0.1'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASSWORD = 'youpassword'
ELASTICSEARCH_CA_CERT_PATH = None
ELASTICSEARCH_TIMEOUT = 3000
ELASTICSEARCH_RETRY = True
ELASTICSEARCH_RETRIES = 5
ELASTICSEARCH_HTTP_COMPRESS = False
ELASTICSEARCH_VERIFY_CERTS = False
ELASTICSEARCH_COMPAT_VERSION = 8  # or 7 if your cluster is Elasticsearch 7.x

# ===== INDEX PATTERN =====
LDAP_INDEX = 'ldap-*'

# ===== DETECTION PARAMETERS =====
# Time window in minutes to look for failures before success
TIME_WINDOW_MINUTES = 10

# Number of failed attempts before success to trigger alert
FAILED_THRESHOLD = 10

# LDAP log field names
FIELD_UID = 'uid.keyword'
FIELD_CLIENT_IP = 'client'
FIELD_RESULT = 'response.error.keyword'  
FIELD_TIMESTAMP = '@timestamp'
FIELD_LDAP_VERB = 'requests.verb.keyword'


DEBUG = False  # or False to silence debug messages

#How long should we lookback in database
LOOKBACK_DAYS = 30

#Page size - Maximum is 10000
SCROLL_PAGE_SIZE = 10000

#Timeout of scrolling
SCROLL_TIMEOUT = "2m"

