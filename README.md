# Instructions


## ASR

**Upload data files into respective folders**
- mp3 files in `base/asr/data/cv-valid-dev` (should have same names as in csv file)
- csv file in `base/asr/data/cv-valid-dev-text/cv-valid-dev.cv`

<br>

**To start flask API using docker:**
- Run from `base/asr` folder to build and up docker
```
./run-docker-compose-asr.sh
```
- Or run from `base/asr` folder respectively

```
docker compose build
docker compose up -d
```

<br>

**To test docker**
- On browser: http://127.0.0.1:8001/ping should return `pong`
- Curl from `base` folder should have output with duration and transcription

```
curl.exe -X POST -F "file=@asr\data\cv-valid-dev\sample-xxxxx.mp3" http://127.0.0.1:8001/asr
```

<br>

**To set up environment for transcribe and save into csv locally**
- Run from `base/asr` folder

```
conda env create -f conda-asr-env.yaml
```

<br>

**To activate environment**
- Run

```
conda activate asr-env
```

<br>

**To transcribe and save into csv**
- Run from `base/asr` folder
```
./run-cv-decode.sh
```

- Or run from `base/asr` folder
```
python src/cv-decode.py
```

Output csv will be `base/asr/data/cv-valid-dev-text/cv-valid-dev-updated.csv`

<br>


## Deployment Design

**Upload processed data file into respective folders**
- csv file in `base/deployment-design/elastic-backend/data/csv-valid-dev-updated.csv`

<br>

**To start ElasticSearch and Search UI using docker:**
- Run From `base/deployment-design` folder to build and up docker
```
./run-docker-compose-react-search.sh
```
- Or run from `base/deployment-design` folder respectively

```
docker compose build
docker compose up -d
```

<br>

**To set up environment for indexing locally**
- Run from `base/deployment-design` folder

```
conda env create -f conda-elastic-backend-env.yaml
```

<br>

**To activate environment**
- Run

```
conda activate elastic-backend-env
```

<br>

**To perform indexing**
- Ensure that docker is running. Wait some time for ElasticSearch to finish loading.
- Run from `base/deployment-design` folder
```
./run-cv-index.sh
```

- Or run from `base/asr` folder
```
python elastic-backend/src/cv-index.py
```

<br>

**To access locally**
- Access index from http://localhost:9200
- Access search from http://localhost:3000

Or replace `localhost` with AWS public address.

<br>

---

## Assumptions
- No need to dockerise where it is not instructed specifically
- Need to write the duration into column `duration`
- No intermediary step required to transfer processed `cv-valid-dev` from `asr` to `deployment-design` data folder. Manual step done.
