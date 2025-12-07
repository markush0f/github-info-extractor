-- Enabled extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Users table
CREATE TABLE public.users (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    username text NOT NULL UNIQUE,
    name text,
    bio text,
    avatar_url text,
    created_at timestamp DEFAULT now(),
    github_username text UNIQUE
);

-- Projects table
CREATE TABLE public.projects (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL,
    repo_name text NOT NULL,
    description text,
    stars integer,
    forks integer,
    last_commit timestamp,
    created_at timestamp DEFAULT now(),
    project_type text NOT NULL DEFAULT 'github',
    source_url text,
    CONSTRAINT projects_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users(id)
);

-- Entities table
CREATE TABLE public.entities (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL,
    project_id uuid,
    type text NOT NULL,
    raw_data jsonb NOT NULL,
    created_at timestamp DEFAULT now(),
    summary text,
    CONSTRAINT entities_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users(id),
    CONSTRAINT entities_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.projects(id)
);

-- Documents table
CREATE TABLE public.documents (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id uuid NOT NULL,
    title text,
    content text NOT NULL,
    created_at timestamp DEFAULT now(),
    CONSTRAINT documents_entity_id_fkey FOREIGN KEY (entity_id)
        REFERENCES public.entities(id)
);

-- Chunks table
CREATE TABLE public.chunks (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id uuid NOT NULL,
    chunk_index integer NOT NULL,
    chunk_text text NOT NULL,
    created_at timestamp DEFAULT now(),
    CONSTRAINT chunks_document_id_fkey FOREIGN KEY (document_id)
        REFERENCES public.documents(id)
);

-- Embeddings table
CREATE TABLE public.embeddings (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    chunk_id uuid NOT NULL,
    embedding vector(1536), -- Changed USER-DEFINED → vector
    created_at timestamp DEFAULT now(),
    CONSTRAINT embeddings_chunk_id_fkey FOREIGN KEY (chunk_id)
        REFERENCES public.chunks(id)
);

-- project_languages table
CREATE TABLE public.project_languages (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id uuid NOT NULL,
    language text NOT NULL,
    bytes bigint,
    created_at timestamp DEFAULT now(),
    CONSTRAINT project_languages_project_id_fkey FOREIGN KEY (project_id)
        REFERENCES public.projects(id)
);

-- user_languages table
CREATE TABLE public.user_languages (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id uuid NOT NULL,
    language text NOT NULL,
    bytes bigint,
    repos_count integer,
    created_at timestamp DEFAULT now(),
    CONSTRAINT user_languages_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users(id)
);

-- languages_stats table
CREATE TABLE public.languages_stats (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    language text NOT NULL UNIQUE,
    total_bytes bigint DEFAULT 0,
    projects_count integer DEFAULT 0,
    users_count integer DEFAULT 0,
    usage_percentage real DEFAULT 0,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now(),
    user_id uuid,
    CONSTRAINT languages_stats_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public.users(id)
);
