create extension if not exists vector
with schema extensions;


create table if not exists
public.documents (

  id bigserial primary key,

  title text not null,

  content text not null,

  source text,

  embedding
    extensions.vector(1536)
    not null,

  created_at
    timestamptz
    default now()
);


create index if not exists
documents_embedding_hnsw

on public.documents

using hnsw (
  embedding
  extensions.vector_cosine_ops
);


create or replace function
public.match_documents (

  query_embedding
    extensions.vector(1536),

  match_threshold
    float,

  match_count
    int
)

returns table (

  id bigint,

  title text,

  content text,

  source text,

  similarity float
)

language sql

stable

as $$

  select

    d.id,

    d.title,

    d.content,

    d.source,

    1 -
    (
      d.embedding
      <=>
      query_embedding
    )
    as similarity

  from public.documents d

  where
    1 -
    (
      d.embedding
      <=>
      query_embedding
    )
    >= match_threshold

  order by
    d.embedding
    <=>
    query_embedding

  limit least(
    match_count,
    50
  );

$$;