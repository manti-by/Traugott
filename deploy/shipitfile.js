module.exports = function (shipit) {
    require('shipit-deploy')(shipit);

    shipit.initConfig({
        default: {
            workspace: '/home/manti/www/traugott/src',
            deployTo: '/home/manti/www/traugott/src',
            repositoryUrl: 'git@github.com:manti-by/Traugott.git',
            ignores: ['.git', 'app/node_modules'],
            rsync: ['--del'],
            keepReleases: 2,
            key: 'keys/deploy',
            shallowClone: true
        },
        staging: {
            servers: 'manti@m53.by'
        }
    });
};