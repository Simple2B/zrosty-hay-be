from typing import TYPE_CHECKING

import uuid

import boto3
import botocore
from pathlib import Path

from flask import Flask
from app.logger import log

if TYPE_CHECKING:
    from app.models import Photo


class S3Bucket:
    def init_app(self, app: Flask):
        self.bucket_name = app.config["AWS_BUCKET_NAME"]
        self.aws_domain = app.config["AWS_S3_DOMAIN"]
        self.app_name = app.config["APP_NAME"]
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=app.config["AWS_ACCESS_KEY"],
            aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"],
        )

    def _generate_img_uid(self):
        return str(uuid.uuid4())

    def create_photo(self, file, folder_name: str = "") -> "Photo":
        log(log.INFO, "Uploading file to s3 bucket")
        from app.models import Photo

        extension_files = file.filename.split(".")[-1]
        original_file_name = file.filename
        uuid = self._generate_img_uid()
        re_file_name = f"{uuid}.{extension_files}"

        img_path = Path("dev")
        if self.app_name == "production":
            img_path = Path("prod")

        img_path = img_path / Path(folder_name) / re_file_name
        try:
            self.s3.upload_fileobj(
                file,
                self.bucket_name,
                str(img_path),
                ExtraArgs={"ContentType": file.content_type},
            )
        except botocore.exceptions.ClientError as error:
            log(log.ERROR, "Error upload file to s3 bucket : [%s]", error.response["Error"]["Message"])
            raise TypeError(error.response["Error"]["Message"])
        url_path = f"https://{self.aws_domain}/{self.bucket_name}/" + str(img_path)

        return Photo(uuid=uuid, original_name=original_file_name, url_path=url_path)

    # def delete_img(self, file_url: str):
    #     file_path = file_url.replace(f"https://{self.bucket_name}/", "").strip()
    #     self.s3.delete_object(Bucket=self.bucket_name, Key=file_path)
