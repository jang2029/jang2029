

from rayvision_api import RayvisionAPI
from rayvision_sync.upload import RayvisionUpload

api = RayvisionAPI(access_id="keyring",
                   access_key="Keyring1!",
                   domain="task.foxrenderfarm.com",
                   platform="2")

UPLOAD = RayvisionUpload(api)
UPLOAD.thread_pool_upload(upload_pool, pool_size=20)