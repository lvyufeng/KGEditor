# get raw data from text

# run entity recognition and relation extraction services
# to get useful triple data

# add triple data into arangodb(tmp data)

from tasks.main import celery_app as app
import requests
import json

@app.task(bind=True)
def annotation_task(self,filepath,model_url):
    """Background task that runs a long function with progress reports."""
    """get the txt's content & model """
    with open(filepath) as fp:
        content = fp.readlines()
        line_num = len(content)
    result = []
    if line_num > 0:
        for i in range (0,line_num):
            res = requests.get(model_url + content[i])
            line_result = json.loads(res.text)['relations']
            result = result+line_result
            self.update_state(state='PROGRESS',
                            meta={'current': i+1, 'total': line_num,
                                    'status': "{0}line completed!".format(i)})
    return {'current': line_num, 'total': line_num, 'status': 'Task completed!',
            'result': result}