from app import db


class Restaurant(db.Model):
    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }

    def __repr__(self):
        return '<Restaurant {0}>'.format(self.name)


class MenuItem(db.Model):
    __tablename__ = 'menu_item'

    name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'price' : self.price,
            'course': self.course,
            'id': self.id,
            'restaurant_id' : self.restaurant_id
        }

    def __repr__(self):
        return '<MenuItem {0}>'.format(self.name)
