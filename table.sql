create table if not exists public.ping
(
    id    serial,
    time  timestamp with time zone default now(),
    delay double precision
);