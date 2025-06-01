from pathlib import Path
import os
import tempfile

def get_default_temp_path() -> str:
    """Return OS-appropriate temporary storage path."""
    temp_dir = Path(tempfile.gettempdir()) / "archive_processing"
    if os.name == "nt":
        return str(temp_dir)
    return "/tmp/archive_processing"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\">
<title>Archive Agent Setup</title>
<style>
body { font-family: Arial, sans-serif; margin: 20px; }
label { display: block; margin-top: 10px; }
textarea { width: 100%; height: 200px; }
</style>
</head>
<body>
<h1>Archive Processing Agent Setup</h1>
<form id=\"setupForm\">
  <label>Storage Provider <input type=\"text\" id=\"STORAGE_PROVIDER\" value=\"azure\"></label>
  <label>Azure Storage Account Name <input type=\"text\" id=\"AZURE_STORAGE_ACCOUNT_NAME\"></label>
  <label>Azure Storage Account Key <input type=\"text\" id=\"AZURE_STORAGE_ACCOUNT_KEY\"></label>
  <label>Azure Key Vault URL <input type=\"text\" id=\"AZURE_KEY_VAULT_URL\"></label>
  <label>Application Environment <input type=\"text\" id=\"APP_ENV\" value=\"development\"></label>
  <label>Log Level <input type=\"text\" id=\"LOG_LEVEL\" value=\"INFO\"></label>
  <label>Max File Size MB <input type=\"number\" id=\"MAX_FILE_SIZE_MB\" value=\"100\"></label>
  <label>Max Archive Files <input type=\"number\" id=\"MAX_ARCHIVE_FILES\" value=\"1000\"></label>
  <label>Temp Storage Path <input type=\"text\" id=\"TEMP_STORAGE_PATH\" value=\"__TEMP_PATH__\"></label>
  <label>Agent Name <input type=\"text\" id=\"AGENT_NAME\" value=\"archive-processing-agent\"></label>
  <label>Agent Version <input type=\"text\" id=\"AGENT_VERSION\" value=\"1.0.0\"></label>
  <label>API Key (enter MANUAL to skip) <input type=\"text\" id=\"AGENT_AUTH_TOKEN\"></label>
  <button type=\"button\" onclick=\"generateEnv()\">Generate .env</button>
</form>
<h2>.env contents</h2>
<pre id=\"output\"></pre>
<h2 id=\"cmdHeader\" style=\"display:none\">Manual Commands</h2>
<pre id=\"command\" style=\"display:none\"></pre>
<h2>Next Steps</h2>
<pre id=\"tests\"></pre>
<script>
function generateEnv() {
  const fields = ['STORAGE_PROVIDER','AZURE_STORAGE_ACCOUNT_NAME','AZURE_STORAGE_ACCOUNT_KEY','AZURE_KEY_VAULT_URL','APP_ENV','LOG_LEVEL','MAX_FILE_SIZE_MB','MAX_ARCHIVE_FILES','TEMP_STORAGE_PATH','AGENT_NAME','AGENT_VERSION','AGENT_AUTH_TOKEN'];
  let env = '';
  let manual = false;
  fields.forEach(function(id){
    const val = document.getElementById(id).value.trim();
    if(id === 'AGENT_AUTH_TOKEN' && val === 'MANUAL') {
      manual = true;
    } else if(val) {
      env += id + '=' + val + '\n';
    }
  });
  document.getElementById('output').textContent = env;

  if(manual) {
    document.getElementById('cmdHeader').style.display = 'block';
    document.getElementById('command').style.display = 'block';
    document.getElementById('command').textContent = 'echo "AGENT_AUTH_TOKEN=<your_key>" >> .env';
  } else {
    document.getElementById('cmdHeader').style.display = 'none';
    document.getElementById('command').style.display = 'none';
  }

  document.getElementById('tests').textContent = 'Run tests with: pytest tests/';
}
</script>
</body>
</html>
"""


def main() -> None:
    target = Path(__file__).with_name("setup.html")
    html = HTML_TEMPLATE.replace("__TEMP_PATH__", get_default_temp_path())
    target.write_text(html, encoding="utf-8")
    print(f"setup.html written to {target}")


if __name__ == "__main__":
    main()
