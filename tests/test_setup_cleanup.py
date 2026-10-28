import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'setup-cerberus.sh'

class SetupCleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.target = self.root / 'target'
        self.env = os.environ.copy()
        for key in list(self.env):
            if key.startswith('GIT_'):
                del self.env[key]
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        (self.source / 'setup-cerberus.sh').write_text(SCRIPT.read_text())
        (self.source / 'README.md').write_text('Fixture only.\n')
        self.git('init', '-q', '-b', 'main')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.source), *args], env=self.env,
                              capture_output=True, text=True, check=True)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')

    def run_setup(self):
        return subprocess.run(['bash', str(self.source / 'setup-cerberus.sh'), str(self.target)],
                              cwd=self.root, env=self.env, capture_output=True, text=True)

    def test_new_empty_target_removed_on_failure(self):
        self.commit()
        result = self.run_setup()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.target.exists())

    def test_preexisting_empty_target_preserved(self):
        self.target.mkdir()
        self.commit()
        self.assertNotEqual(self.run_setup().returncode, 0)
        self.assertTrue(self.target.is_dir())

    def test_preexisting_user_data_preserved(self):
        self.target.mkdir()
        data = self.target / 'user-data.txt'
        data.write_text('keep')
        self.commit()
        self.assertNotEqual(self.run_setup().returncode, 0)
        self.assertEqual(data.read_text(), 'keep')

    def test_success_retains_target(self):
        for name in ['CONTRIBUTING.md', 'SECURITY.md', '.gitignore', 'docs/index.md',
                     'templates/index.md', 'scripts/index.txt', '.github/index.txt',
                     'research/.gitkeep', 'reports/.gitkeep']:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Fixture.\n')
        (self.source / '.gitignore').write_text('')
        self.commit()
        result = self.run_setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / '.git').is_dir())

if __name__ == '__main__':
    unittest.main()
