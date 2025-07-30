import sys
from unittest import mock

import src.id as id_mod

def test_get_user_by_spec_name():
    with mock.patch('pwd.getpwnam') as mock_getpwnam:
        mock_getpwnam.return_value = mock.Mock(pw_name='testuser', pw_uid=1000, pw_gid=1000)
        user, err = id_mod.get_user_by_spec('testuser')
        assert err is None
        assert user.pw_name == 'testuser'

def test_get_user_by_spec_uid():
    with mock.patch('pwd.getpwuid') as mock_getpwuid:
        mock_getpwuid.return_value = mock.Mock(pw_name='testuser', pw_uid=1000, pw_gid=1000)
        user, err = id_mod.get_user_by_spec('1000')
        assert err is None
        assert user.pw_uid == 1000

def test_get_user_by_spec_invalid():
    with mock.patch('pwd.getpwnam', side_effect=KeyError):
        user, err = id_mod.get_user_by_spec('nouser')
        assert user is None
        assert "no such user" in err

def test_print_id_user_name(capsys):
    with mock.patch('pwd.getpwuid') as mock_getpwuid:
        mock_getpwuid.return_value = mock.Mock(pw_name='testuser')
        id_mod.print_id(1000, 'user', use_name=True)
        out, _ = capsys.readouterr()
        assert out == 'testuser'

def test_print_id_group_name(capsys):
    with mock.patch('grp.getgrgid') as mock_getgrgid:
        mock_getgrgid.return_value = mock.Mock(gr_name='testgroup')
        id_mod.print_id(1000, 'group', use_name=True)
        out, _ = capsys.readouterr()
        assert out == 'testgroup'

def test_print_id_user_number(capsys):
    id_mod.print_id(1000, 'user', use_name=False)
    out, _ = capsys.readouterr()
    assert out == '1000'

def test_print_group_list_names(capsys):
    with mock.patch('pwd.getpwnam') as mock_getpwnam, \
         mock.patch('os.getgrouplist') as mock_getgrouplist, \
         mock.patch('grp.getgrgid') as mock_getgrgid:
        mock_getpwnam.return_value = mock.Mock(pw_gid=1000)
        mock_getgrouplist.return_value = [1000, 1001]
        mock_getgrgid.side_effect = [mock.Mock(gr_name='group1'), mock.Mock(gr_name='group2')]
        id_mod.print_group_list('testuser', use_name=True, delimiter=',')
        out, _ = capsys.readouterr()
        assert out == 'group1,group2'

def test_print_group_list_numbers(capsys):
    with mock.patch('pwd.getpwnam') as mock_getpwnam, \
         mock.patch('os.getgrouplist') as mock_getgrouplist:
        mock_getpwnam.return_value = mock.Mock(pw_gid=1000)
        mock_getgrouplist.return_value = [1000, 1001]
        id_mod.print_group_list('testuser', use_name=False, delimiter=' ')
        out, _ = capsys.readouterr()
        assert out == '1000 1001'

def test_print_full_info(capsys):
    with mock.patch('pwd.getpwuid') as mock_getpwuid, \
         mock.patch('grp.getgrgid') as mock_getgrgid, \
         mock.patch('os.getgroups') as mock_getgroups:
        mock_getpwuid.side_effect = [mock.Mock(pw_name='user')] * 2
        mock_getgrgid.side_effect = [mock.Mock(gr_name='group')] * 2
        mock_getgroups.return_value = [1000, 1001]
        id_mod.print_full_info(1000, 1000, 1000, 1000)
        out, _ = capsys.readouterr()
        assert 'uid=1000(user)' in out
        assert 'gid=1000(group)' in out
        assert 'groups=1000(group),1001(group)' in out
