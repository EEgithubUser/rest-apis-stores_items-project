from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    # use @blp.response when you are RETURNING something!
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required() # Destructive operations should be accompanied by jwt_required for safety
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(item_id)
        #raise NotImplementedError("Deleting an item is not implemented.")
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema) # Note: response decorator must be DEEPER than arguments decorator
    # arguments decorator MUST GO IN FRONT of the root arguments (item_id)
    # in this case for ItemUpdateSchema (item_data) must go before item_id
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    # returning multiple item schemas use many=True
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        # only need to return items.values() b/c the blp response many=True turns the dict into a list
        #return {"items": list(items.values())}
        #return items.values()
        return ItemModel.query.all()

    @jwt_required(fresh=True) # Must send JWT if you want to use this endpoint
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    # item_data that is passed in (can be called w/e) is going to contain the JSON data that is
    # filtered through the validated fields that the schema requested
    # JSON is passed through the ItemSchema, checks fields are there and valid
    # and gives this method an argument (item_data), which is a vaid dictionary (Python)
    def post(self, item_data):
        # can delete request.get_json() item data now that we have the item_data argument from schema
        #item_data = request.get_json()
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item
    


    