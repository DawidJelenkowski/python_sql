-- Active: 1687340072719@@postgres@5432@guestbook

create table
    if not exists users (
        id serial PRIMARY KEY,
        email text NOT NULL UNIQUE,
        password text NOT NULL,
        active boolean NOT NULL DEFAULT false,
        created_at timestamp DEFAULT current_timestamp,
        activated_at timestamp
    );

create table
    if not exists tokens (
        id serial PRIMARY KEY,
        token text NOT NULL,
        user_id integer NOT NULL REFERENCES users (id) ON DELETE CASCADE,
        created_at timestamp NOT NULL DEFAULT current_timestamp
    );

create table
    if not exists guestbook (
        id serial PRIMARY KEY,
        message text NOT NULL,
        user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        private boolean NOT NULL DEFAULT false,
        created_at timestamp NOT NULL DEFAULT current_timestamp,
        updated_at timestamp
    );