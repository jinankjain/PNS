import zipfile
import io


def _alexa_etl():
    with zipfile.ZipFile('top-1m.csv.zip') as zfile:
        buf = io.BytesIO(zfile.read('top-1m.csv'))
        for line in buf:
            line_str = line.decode('utf-8')
            (rank, domain) = line_str.split(',')
            yield domain.strip()


def get_top_domains(num=100):
    domain_generator = _alexa_etl()
    return [next(domain_generator) for _ in range(num)]

if __name__ == "__main__":
    print(get_top_domains(10))
