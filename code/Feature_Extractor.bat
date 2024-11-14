@echo off
call activate fe_env
python "Radiomics_Feature_Extractor.py"
call conda deactivate
