# Notes on my Photo Workflow

Notes for myself on my photo workflow. Partly useful as the raison d'etre for the scripts in this repo, partly useful as notes on how to process photos.

## 1. Copy files from SD to a `TO_PROCESS/YYYY/YYYY.MM - {TITLE}/` folder
## 2. Run EOG (Eye Of Gnome), remove JPGs that are obviously bad
## 3. Run `remove-unneeded-raws.py`

To remove RAWs for which the JPG was removed in the first selection

## 4. Open Darktable

### Import Files
* import folder, set metadata tags in the import dialog

### Other activities
* select "show all except rejected"
* process either the RAW or the JPG for each file
* remove the JPG (if RAW was processed) or RAW (vice versa)
* remove both if the picture is not that good in the end
* once processing is finished, export in the `darktable_exported` directory

## 5. Run `remove-downvoted-pics.py`

To remove pictures completely removed in darktable (both RAW and JPG)

## 6. Upload `darktable_exported` pics to Google Photos
## 7. Move from `TO_PROCESS` to `PROCESSED`
## 8. From time to time, backup `PROCESSED`
