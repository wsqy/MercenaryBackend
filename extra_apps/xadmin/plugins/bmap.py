from django.conf import settings

from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CreateAdminView, UpdateAdminView


class BMapPlugin(BaseAdminPlugin):
    open_bmap = False

    def init_request(self, *args, **kwargs):
        return bool(self.open_bmap)

    # 插件拦截了返回 Media 的方法，加入自己需要的 js 文件。
    def get_media(self, media):
        media.add_css({'all': [self.static('bmap/location_picker.css'),]})

        media.add_js([
            # '//cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
            '//api.map.baidu.com/api?v=2.0&ak={}'.format(settings.BMAP_KEY),
            self.static('bmap/location_picker_xadmin.js'),
        ])
        return media



site.register_plugin(BMapPlugin, CreateAdminView)
site.register_plugin(BMapPlugin, UpdateAdminView)
