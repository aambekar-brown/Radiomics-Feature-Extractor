@echo off
call activate venv3_7
python "Radiomics_Feature_Extractor.py"
call conda deactivate