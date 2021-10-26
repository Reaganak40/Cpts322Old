from app import create_app, db
from app.Model.models import Post, Tag, postTags

app = create_app()

# ================================================================
#   Name:           Init DB
#   Description:    If there is not db, call this function to initialize it
#   Last Changed:   10/26/21
#   Changed By:     Reagan Kelley
#   Change Details: Skeleton version for initDB (taken from smileApp)
#=================================================================
@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
         tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship'] ##NEED TO: change tag names
         for t in tags:
             db.session.add(Tag(name=t))
         db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)