from flask_assets import Environment,Bundle

def bundle_css_files(app):
    assets =Environment(app)

    css_bundle = Bundle('css/*.css', filters='cssmin', output='gen/bundled.css')
    assets.register('css_all', css_bundle)
    css_bundle.build()