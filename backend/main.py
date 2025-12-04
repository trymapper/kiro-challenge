from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import boto3
from boto3.dynamodb.conditions import Attr
import os
from datetime import datetime

app = FastAPI(title="Event Management API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DynamoDB設定
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'EventsTable')
table = dynamodb.Table(table_name)


# Pydanticモデル
class Event(BaseModel):
    eventId: str = Field(..., pattern=r'^[a-zA-Z0-9\-_]+$')
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., max_length=1000)
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    location: str = Field(..., min_length=1, max_length=200)
    capacity: int = Field(..., gt=0)
    organizer: str = Field(..., min_length=1, max_length=100)
    status: str = Field(..., pattern=r'^(active|cancelled|completed)$')


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, gt=0)
    organizer: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = Field(None, pattern=r'^(active|cancelled|completed)$')


@app.get("/")
async def root():
    return {"message": "Event Management API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/events", status_code=status.HTTP_200_OK)
async def get_events(status_filter: Optional[str] = None):
    """全イベントを取得（オプションでステータスフィルタ）"""
    try:
        if status_filter:
            response = table.scan(
                FilterExpression=Attr('event_status').eq(status_filter)
            )
        else:
            response = table.scan()
        
        events = response.get('Items', [])
        
        # DynamoDBのフィールド名を元に戻す
        formatted_events = []
        for event in events:
            formatted_events.append({
                'eventId': event.get('eventId'),
                'title': event.get('title'),
                'description': event.get('event_description'),
                'date': event.get('event_date'),
                'location': event.get('event_location'),
                'capacity': event.get('event_capacity'),
                'organizer': event.get('organizer'),
                'status': event.get('event_status')
            })
        
        return formatted_events
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve events: {str(e)}"
        )


@app.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(event: Event):
    """新しいイベントを作成"""
    try:
        # DynamoDBの予約語を避けるためフィールド名を変更
        item = {
            'eventId': event.eventId,
            'title': event.title,
            'event_description': event.description,
            'event_date': event.date,
            'event_location': event.location,
            'event_capacity': event.capacity,
            'organizer': event.organizer,
            'event_status': event.status
        }
        
        table.put_item(Item=item)
        
        return {
            'eventId': event.eventId,
            'title': event.title,
            'description': event.description,
            'date': event.date,
            'location': event.location,
            'capacity': event.capacity,
            'organizer': event.organizer,
            'status': event.status
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        )


@app.get("/events/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(event_id: str):
    """特定のイベントを取得"""
    try:
        response = table.get_item(Key={'eventId': event_id})
        
        if 'Item' not in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found"
            )
        
        event = response['Item']
        return {
            'eventId': event.get('eventId'),
            'title': event.get('title'),
            'description': event.get('event_description'),
            'date': event.get('event_date'),
            'location': event.get('event_location'),
            'capacity': event.get('event_capacity'),
            'organizer': event.get('organizer'),
            'status': event.get('event_status')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve event: {str(e)}"
        )


@app.put("/events/{event_id}", status_code=status.HTTP_200_OK)
async def update_event(event_id: str, event_update: EventUpdate):
    """イベントを更新"""
    try:
        # イベントが存在するか確認
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found"
            )
        
        # 更新する属性を構築
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        update_fields = event_update.model_dump(exclude_unset=True)
        
        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        field_mapping = {
            'description': 'event_description',
            'date': 'event_date',
            'location': 'event_location',
            'capacity': 'event_capacity',
            'status': 'event_status'
        }
        
        for idx, (field, value) in enumerate(update_fields.items()):
            db_field = field_mapping.get(field, field)
            if idx > 0:
                update_expression += ", "
            update_expression += f"#{db_field} = :{db_field}"
            expression_attribute_names[f"#{db_field}"] = db_field
            expression_attribute_values[f":{db_field}"] = value
        
        table.update_item(
            Key={'eventId': event_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        # 更新後のイベントを取得
        response = table.get_item(Key={'eventId': event_id})
        event = response['Item']
        
        return {
            'eventId': event.get('eventId'),
            'title': event.get('title'),
            'description': event.get('event_description'),
            'date': event.get('event_date'),
            'location': event.get('event_location'),
            'capacity': event.get('event_capacity'),
            'organizer': event.get('organizer'),
            'status': event.get('event_status')
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update event: {str(e)}"
        )


@app.delete("/events/{event_id}", status_code=status.HTTP_200_OK)
async def delete_event(event_id: str):
    """イベントを削除"""
    try:
        # イベントが存在するか確認
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Event with id {event_id} not found"
            )
        
        table.delete_item(Key={'eventId': event_id})
        
        return {"message": f"Event {event_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete event: {str(e)}"
        )
