python setup.py sdist bdist_wheel
python -m twine upload dist/*

rm -rf build
rm -rf dist
rm -rf tracardi_google_sheets_integrator.egg-info
