# Nomark - Notion to markdown exporter

![https://drive.google.com/uc?export=view&id=14gTzk41cknPvfYvvzQIEODFEpnjs51Ny](https://drive.google.com/uc?export=view&id=14gTzk41cknPvfYvvzQIEODFEpnjs51Ny)

**Nomark** is the Notion to markdown exporter with image hosting use google drive. 
Use the notion as a WYSIWYG editor for a static blog with no matter about uploading images.

This readme is also written in notion and exported by using the Nomark. 
[https://abit.ly/nomark-example](https://abit.ly/nomark-example) ← check this

## How to use

1. Install nomark

```python
pip install nomark
```

2. Download the google drive api token

[https://developers.google.com/drive/api/v3/quickstart/python](https://developers.google.com/drive/api/v3/quickstart/python) 
Visit link to enable google drive api. Click the "Enable the Drive API" and download the `credential.json` in to `~/.cred/credential.json`

![https://drive.google.com/uc?export=view&id=1Hl7_NANm9wGzcC9wEv9JhOMudBGmCCUO](https://drive.google.com/uc?export=view&id=1Hl7_NANm9wGzcC9wEv9JhOMudBGmCCUO)

3. Get your notion api token

You need to obtain your token for using notion api.
Go to [http://notion.so](http://notion.so) and open chrome developer tools. Open "Application" tab → "Storage" → "Cookies" and copy the `token_v2` Value.

And export the notion token to variable  `export NOTION_TOKEN=token_v2_value`. Paste it in to `~/.bashrc`

4. Get notion article url

![https://drive.google.com/uc?export=view&id=1_qIJW7Bp9FrKu8QpEnne5fqYgthbaWVI](https://drive.google.com/uc?export=view&id=1_qIJW7Bp9FrKu8QpEnne5fqYgthbaWVI)

Set your article shareable and copy the link.

5. Run nomark

```bash
$ nomark http://www.notion.so/your_article_url
```

## Requirements

python 3.7+
