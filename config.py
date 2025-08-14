# ===== ELASTICSEARCH CONNECTION =====
ELASTICSEARCH_HOST = '192.168.1.1'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASSWORD = 'yourpassword'
ELASTICSEARCH_CA_CERT_PATH = None
ELASTICSEARCH_TIMEOUT = 300
ELASTICSEARCH_RETRY = True
ELASTICSEARCH_RETRIES = 5
ELASTICSEARCH_HTTP_COMPRESS = False
ELASTICSEARCH_VERIFY_CERTS = False

# ===== INDEX PATTERN =====
LDAP_INDEX = 'ldap-*'

# ===== DETECTION PARAMETERS =====
# Time window in minutes to look for failures before success
TIME_WINDOW_MINUTES = 5

# Number of failed attempts before success to trigger alert
FAILED_THRESHOLD = 5

# LDAP log field names
FIELD_UID = 'uid'
FIELD_CLIENT_IP = 'client'
FIELD_RESULT = 'result'   # Example: could be 'success' or 'fail'
FIELD_TIMESTAMP = '@timestamp'
