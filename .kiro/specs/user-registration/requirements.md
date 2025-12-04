# Requirements Document

## Introduction

このドキュメントは、イベント管理システムにおけるユーザー登録機能の要件を定義します。ユーザーはイベントに登録・登録解除でき、定員制限とキャンセル待ちリスト機能をサポートします。

## Glossary

- **User**: システムを利用してイベントに登録する個人
- **Event**: ユーザーが登録できる活動またはイベント
- **Registration**: ユーザーとイベント間の関連付け
- **Capacity**: イベントに参加できる最大ユーザー数
- **Waitlist**: イベントが満員の場合にユーザーが待機するリスト
- **System**: イベント管理APIシステム

## Requirements

### Requirement 1

**User Story:** As a system administrator, I want to create users with basic information, so that they can register for events.

#### Acceptance Criteria

1. WHEN a user is created with a userId and name THEN the System SHALL store the user information in the database
2. WHEN a user is created with a duplicate userId THEN the System SHALL reject the creation and return an error
3. WHEN a user is created with an empty or invalid userId THEN the System SHALL reject the creation and return a validation error
4. WHEN a user is created with an empty or invalid name THEN the System SHALL reject the creation and return a validation error

### Requirement 2

**User Story:** As an event organizer, I want to set capacity limits for events with optional waitlists, so that I can manage event attendance effectively.

#### Acceptance Criteria

1. WHEN an event is created with a capacity limit THEN the System SHALL enforce the maximum number of registrations
2. WHEN an event is created with a waitlist enabled THEN the System SHALL allow users to join the waitlist when capacity is reached
3. WHEN an event is created without a waitlist THEN the System SHALL reject registration attempts when capacity is reached
4. WHEN an event capacity is set to zero or negative THEN the System SHALL reject the event creation

### Requirement 3

**User Story:** As a user, I want to register for events, so that I can participate in activities I'm interested in.

#### Acceptance Criteria

1. WHEN a user registers for an event with available capacity THEN the System SHALL create a registration record
2. WHEN a user attempts to register for the same event twice THEN the System SHALL reject the duplicate registration
3. WHEN a user registers for a non-existent event THEN the System SHALL return an error
4. WHEN a non-existent user attempts to register THEN the System SHALL return an error

### Requirement 4

**User Story:** As a user, I want to be denied registration when an event is full, so that capacity limits are respected.

#### Acceptance Criteria

1. WHEN a user attempts to register for a full event without a waitlist THEN the System SHALL reject the registration
2. WHEN a user attempts to register for a full event THEN the System SHALL return a clear error message indicating the event is full
3. WHEN the last available spot is taken THEN the System SHALL update the event status to full

### Requirement 5

**User Story:** As a user, I want to be added to a waitlist when an event is full, so that I have a chance to attend if spots become available.

#### Acceptance Criteria

1. WHEN a user attempts to register for a full event with a waitlist enabled THEN the System SHALL add the user to the waitlist
2. WHEN a user is added to the waitlist THEN the System SHALL record the waitlist position
3. WHEN a user is already on the waitlist THEN the System SHALL reject duplicate waitlist entries
4. WHEN a user on the waitlist attempts to register again THEN the System SHALL return an error indicating they are already on the waitlist

### Requirement 6

**User Story:** As a user, I want to unregister from events, so that I can free up my spot if I can no longer attend.

#### Acceptance Criteria

1. WHEN a user unregisters from an event THEN the System SHALL remove the registration record
2. WHEN a user unregisters from an event with a waitlist THEN the System SHALL promote the first waitlisted user to registered status
3. WHEN a user attempts to unregister from an event they are not registered for THEN the System SHALL return an error
4. WHEN the first waitlisted user is promoted THEN the System SHALL notify the change in registration status

### Requirement 7

**User Story:** As a user, I want to view all events I'm registered for, so that I can keep track of my commitments.

#### Acceptance Criteria

1. WHEN a user requests their registered events THEN the System SHALL return a list of all events they are registered for
2. WHEN a user requests their registered events THEN the System SHALL include event details (title, date, location, status)
3. WHEN a user has no registrations THEN the System SHALL return an empty list
4. WHEN a non-existent user requests their events THEN the System SHALL return an error

### Requirement 8

**User Story:** As a user, I want to view my waitlist status, so that I know my position for events I'm waiting to join.

#### Acceptance Criteria

1. WHEN a user requests their waitlist status THEN the System SHALL return all events they are waitlisted for
2. WHEN a user is on a waitlist THEN the System SHALL include their position in the waitlist
3. WHEN a user has no waitlist entries THEN the System SHALL return an empty list

### Requirement 9

**User Story:** As an event organizer, I want to view all registrations for an event, so that I can manage attendees.

#### Acceptance Criteria

1. WHEN an organizer requests registrations for an event THEN the System SHALL return all registered users
2. WHEN an organizer requests registrations for an event THEN the System SHALL include user details (userId, name)
3. WHEN an organizer requests registrations for an event with a waitlist THEN the System SHALL include waitlisted users separately
4. WHEN an event has no registrations THEN the System SHALL return an empty list

### Requirement 10

**User Story:** As a system, I want to maintain data consistency, so that registration information is always accurate.

#### Acceptance Criteria

1. WHEN a registration is created or deleted THEN the System SHALL update the event's current registration count
2. WHEN a user is promoted from waitlist THEN the System SHALL atomically update both registration and waitlist records
3. WHEN concurrent registration attempts occur THEN the System SHALL handle race conditions correctly
4. WHEN a registration operation fails THEN the System SHALL rollback any partial changes
