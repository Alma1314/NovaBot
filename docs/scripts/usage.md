```bash
bash scripts/upload-doc-images-to-r2.sh \
    --remote bulinbot-docs-s3 \
    --bucket bulinbot \
    --prefix docs \
    --rewrite-markdown \
    --public-base-url https://files.bulinbot.app
```