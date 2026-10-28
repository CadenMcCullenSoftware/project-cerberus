import shlex
import shutil
import unittest

import test_setup_cleanup as cleanup


class NonemptyFailureTests(unittest.TestCase):
    def test_new_target_with_data_is_preserved_after_archive_failure(self):
        fixture = cleanup.SetupCleanupTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.commit()
        bin_dir = fixture.root / 'bin'
        bin_dir.mkdir()
        marker = fixture.target / 'partial-data.txt'
        wrapper = bin_dir / 'git'
        real_git = shutil.which('git', path=fixture.env.get('PATH'))
        self.assertIsNotNone(real_git)
        wrapper.write_text(
            '#!/usr/bin/env bash\n'
            'if [[ ${3-} == cat-file ]]; then exit 0; fi\n'
            'if [[ ${3-} == archive ]]; then\n'
            '  printf \'preserve me\' > ' + shlex.quote(str(marker)) + '\n'
            '  exit 23\n'
            'fi\n'
            'exec ' + shlex.quote(real_git) + ' "$@"\n'
        )
        wrapper.chmod(0o755)
        fixture.env['PATH'] = str(bin_dir) + ':' + fixture.env.get('PATH', '')
        result = fixture.run_setup()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertTrue(fixture.target.is_dir(), result.stderr)
        self.assertEqual(marker.read_text(), 'preserve me')


if __name__ == '__main__':
    unittest.main()
