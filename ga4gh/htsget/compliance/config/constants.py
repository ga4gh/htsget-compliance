# HTTP STATUS CODES
STATUS_OK = 200
STATUS_NOT_FOUND = 404

# SCHEMA FILENAMES
SCHEMA_HTSGET_URL = "htsgetUrl.json"
SCHEMA_HTSGET_RESPONSE = "htsgetResponse.json"

ENDPOINTS = ["reads", "variants"]

BASE_URL = "{base_url}/"
READS_URL = BASE_URL + "reads/{obj_id}"
VARIANTS_URL = BASE_URL + "variants/{obj_id}"

READS_ID_FOUND_1 = "10X_P4_0_possorted_genome.bam"
READS_ID_FOUND_2 = "10X_P4_0_possorted_genome.bam"
READS_ID_NOTFOUND_1 = "notfound123456789"
READS_ID_NOTFOUND_2 = "notfound987654321"
