import io
import uuid
from urllib.parse import urljoin

import filetype
import boto3
import botocore
from pathlib import Path

from app import models as m

from app.logger import log
from config import BaseConfig


class S3Bucket:
    bucket_name: str
    aws_domain: str
    aws_s3_base_dir: Path
    s3: boto3.client

    def init_app(self, config: BaseConfig):
        self.bucket_name = config.AWS_BUCKET_NAME
        self.aws_domain = config.AWS_S3_DOMAIN
        self.aws_s3_base_dir = Path("prod") if config.APP_NAME == "production" else Path("dev")
        self.s3 = boto3.client(
            "s3", aws_access_key_id=config.AWS_ACCESS_KEY, aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
        )
        self.aws_s3_base_url = urljoin(f"https://{self.aws_domain}", f"{self.bucket_name}/")

    def _generate_img_uid(self):
        return str(uuid.uuid4())

    def create_photo(self, file: io.BytesIO, file_name: str | None = None, folder_name: str = "") -> m.Photo:
        log(log.INFO, "Uploading file to s3 bucket")

        file_type = filetype.guess(file)

        uuid = self._generate_img_uid()
        re_file_name = f"{uuid}.{file_type.extension}"

        img_path = self.aws_s3_base_dir / Path(folder_name) / re_file_name

        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                str(img_path),
                ExtraArgs={"ContentType": file_type.mime},
            )
        except botocore.exceptions.ClientError as error:
            log(log.ERROR, "Error upload file to s3 bucket : [%s]", error.response["Error"]["Message"])
            raise TypeError(error.response["Error"]["Message"])

        return m.Photo(uuid=uuid, original_name=file_name, url_path=urljoin(self.aws_s3_base_url, str(img_path)))
