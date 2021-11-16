from app import create_app, db
from app.Model.models import Post, Major, Field, postMajors

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
    if Major.query.count() == 0:
         majors = ['Computer Science','Computer Engineering', 'Electrical Engineering', 'Chemical Engineering'] ##NEED TO: change tag names
         for m in majors:
             db.session.add(Major(name=m))
         db.session.commit()

    # if Field.query.count() is None:
    #     field_name = [{'field_name':'Artificial Intelligence', 'major_name':'Computer Science'}]
    #     for f in field_name:
    #         db.session.add(Field(majors = f['majors'], field = f['field']))
    #     db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)