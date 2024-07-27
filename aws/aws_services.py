import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.exceptions import NoCredentialsError


def handle_s3(dataframe, bucket, access_key, secret_key, aws_session_token, action, object_name=None, prefix=None):

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=aws_session_token
    )
    s3_client = session.client('s3')
    list_files = []
    try:

        if action == 'upload':
            import io
            parquet_buffer = io.BytesIO()
            # Converter o DataFrame para Parquet
            pq.write_table(pa.Table.from_pandas(dataframe), parquet_buffer)
            parquet_buffer.seek(0)

            # parquet_buffer = pq.write_table(pa.Table.from_pandas(dataframe)).to_buffer()

            # upload to s3
            # s3 = boto3.client("s3")
            # s3.up
            s3_client.upload_fileobj(
                Fileobj=parquet_buffer,
                Bucket=bucket,
                Key=prefix
            )
        #
        #     if object_name is None:
        #
        #         object_name = file_name.split('/')[-1]
        #
        #     if prefix:
        #
        #         object_name = f"{prefix}/{object_name}"
        #
        #     s3_client.upload_file(file_name, bucket, object_name)

        elif action == 'delete':

            if object_name is None or prefix:
                raise ValueError(
                    "Para deletar um objeto, o 'object_name' deve ser especificado e 'prefix' deve ser None ou vazio."
                )

            s3_client.delete_object(Bucket=bucket, Key=object_name)

        elif action == 'list':

            paginator = s3_client.get_paginator('list_objects_v2')

            for page in paginator.paginate(Bucket=bucket, Prefix=prefix):

                for obj in page.get('Contents', []):

                    print(obj['Key'])
                    list_files.append(obj)

        else:

            print(f"Ação '{action}' não reconhecida.")

            return False

    except NoCredentialsError:

        print("As credenciais não estão disponíveis")

        return False

    except ValueError as ve:

        print(ve)

        return False

    except Exception as e:

        print(f"Erro ao realizar ação '{action}' no arquivo: {e}")

        return False

    if list_files:
        return list_files
    return True
