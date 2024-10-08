from src.database.models import Actor, Contacts
from src import db, app


def new_contact():
    radcliffe_inst = Contacts(
        actor_id=1,
        social_media='https://www.instagram.com/danielradcliffe/',
        publicist_agent_info='ARG Talent Agency'
    )
    radcliffe_tw = Contacts(
        actor_id=1,
        social_media='https://twitter.com/DanielRadcliffe',
        publicist_agent_info='ARG Talent Agency')
    grint = Contacts(
        actor_id=2,
        social_media='https://www.instagram.com/rupertgrint/'
    )
    watson_inst = Contacts(
        actor_id=4,
        social_media='https://www.instagram.com/emmawatson/',
        publicist_agent_info='United Talent Agency (UTA)'
    )
    watson_tw = Contacts(
        actor_id=4,
        social_media='https://twitter.com/EmmaWatson',
        publicist_agent_info='United Talent Agency (UTA)'
    )
    isaacs_inst = Contacts(
        actor_id=5,
        social_media='https://www.instagram.com/jasonisaacs/'
    )
    isaacs_tw = Contacts(
        actor_id=5,
        social_media='https://twitter.com/jasonisaacs'
    )
    pattinson = Contacts(
        actor_id=7,
        publicist_agent_info='William Morris Endeavor (WME)'
    )
    linch_tw = Contacts(
        actor_id=8,
        social_media='https://twitter.com/Evy_Lynch'
    )
    linch_inst = Contacts(
        actor_id=8,
        social_media='https://www.instagram.com/msevylynch/'
    )

    db.session.add(radcliffe_inst)
    db.session.add(radcliffe_tw)
    db.session.add(grint)
    db.session.add(watson_inst)
    db.session.add(watson_tw)
    db.session.add(isaacs_inst)
    db.session.add(isaacs_tw)
    db.session.add(pattinson)
    db.session.add(linch_inst)
    db.session.add(linch_tw)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Populating db...')
    with app.app_context():
        db.create_all()

        new_contact()
        print('Successfully populated!')
