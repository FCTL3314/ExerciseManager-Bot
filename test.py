import polib

po_file_path = "locales/en/LC_MESSAGES/messages.po"
mo_file_path = "locales/en/LC_MESSAGES/messages.mo"

po = polib.pofile(po_file_path)
po.save_as_mofile(mo_file_path)

print(f"Compiled {po_file_path} to {mo_file_path}")
