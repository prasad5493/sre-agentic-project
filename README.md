# Evidence Folder

Place screenshots of the real AWS deployment here. Any PNG or JPG file added
to this folder is automatically picked up by `pages/build_dashboard.py` and
shown in an "Evidence" section on the published page. No code changes are
needed, just add the image files and push.

## Naming the files

Files are displayed in alphabetical order, and the caption under each image
is generated from the filename. Start each filename with a number so they
appear in a sensible order, and use dashes or underscores between words,
which are converted into spaces automatically.

Suggested filenames:

```
01-cloudformation-stack-complete.png
02-cloudformation-resources.png
03-cloudformation-template.png
04-iam-role-permissions.png
05-cloudformation-outputs.png
```

These would appear on the page as:

```
Cloudformation Stack Complete
Cloudformation Resources
Cloudformation Template
Iam Role Permissions
Cloudformation Outputs
```

## Notes

- Keep screenshots reasonably sized, under 1 to 2 MB each, so the page loads
  quickly.
- Crop out anything you do not want visible, such as your AWS account ID or
  billing information, before adding a screenshot here.
- This folder can be left empty. The Evidence section simply will not appear
  on the page until at least one image is added.
