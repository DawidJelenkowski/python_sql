create table if not exists users
(
    id           SERIAL PRIMARY KEY,
    email        TEXT    NOT NULL,
    password     TEXT    NOT NULL,
    active       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMP        DEFAULT current_timestamp,
    activated_at TIMESTAMP
);

create table if not exists tokens
(
    id         serial PRIMARY KEY,
    token      text      NOT NULL,
    user_id    integer   NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    created_at timestamp NOT NULL DEFAULT current_timestamp
);
