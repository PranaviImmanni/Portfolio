-- =====================================================
-- Professional Spotify Data Analysis Database Schema
-- =====================================================
-- This schema follows industry best practices for music streaming analytics
-- Includes proper indexing, constraints, and data types for production use

-- Enable UUID extension for PostgreSQL
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CORE ENTITIES
-- =====================================================

-- Artists table with comprehensive metadata
CREATE TABLE artists (
    artist_id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genres TEXT[],
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    followers_count INTEGER DEFAULT 0,
    market VARCHAR(10),
    spotify_uri VARCHAR(255),
    external_urls JSONB,
    images JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Albums with release information
CREATE TABLE albums (
    album_id VARCHAR(50) PRIMARY KEY,
    album_name VARCHAR(255) NOT NULL,
    artist_id VARCHAR(50) REFERENCES artists(artist_id) ON DELETE CASCADE,
    album_type VARCHAR(50),
    total_tracks INTEGER,
    release_date DATE,
    release_date_precision VARCHAR(10),
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    spotify_uri VARCHAR(255),
    external_urls JSONB,
    images JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tracks with comprehensive audio features
CREATE TABLE tracks (
    track_id VARCHAR(50) PRIMARY KEY,
    track_name VARCHAR(255) NOT NULL,
    artist_id VARCHAR(50) REFERENCES artists(artist_id) ON DELETE CASCADE,
    album_id VARCHAR(50) REFERENCES albums(album_id) ON DELETE CASCADE,
    disc_number INTEGER DEFAULT 1,
    track_number INTEGER,
    duration_ms INTEGER CHECK (duration_ms > 0),
    popularity INTEGER CHECK (popularity >= 0 AND popularity <= 100),
    
    -- Audio features (0.0 to 1.0 scale)
    danceability DECIMAL(3,2) CHECK (danceability >= 0.0 AND danceability <= 1.0),
    energy DECIMAL(3,2) CHECK (energy >= 0.0 AND energy <= 1.0),
    valence DECIMAL(3,2) CHECK (valence >= 0.0 AND valence <= 1.0),
    acousticness DECIMAL(3,2) CHECK (acousticness >= 0.0 AND acousticness <= 1.0),
    instrumentalness DECIMAL(3,2) CHECK (instrumentalness >= 0.0 AND instrumentalness <= 1.0),
    liveness DECIMAL(3,2) CHECK (liveness >= 0.0 AND liveness <= 1.0),
    speechiness DECIMAL(3,2) CHECK (speechiness >= 0.0 AND speechiness <= 1.0),
    
    -- Musical attributes
    tempo DECIMAL(5,2) CHECK (tempo > 0),
    key INTEGER CHECK (key >= -1 AND key <= 11),
    mode INTEGER CHECK (mode IN (0, 1)),
    time_signature INTEGER CHECK (time_signature >= 3 AND time_signature <= 7),
    
    -- Metadata
    spotify_uri VARCHAR(255),
    external_urls JSONB,
    is_explicit BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- USER BEHAVIOR & STREAMING
-- =====================================================

-- User profiles (if using personal data)
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(255),
    country VARCHAR(10),
    birth_year INTEGER CHECK (birth_year >= 1900 AND birth_year <= 2024),
    gender VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Streaming history with comprehensive context
CREATE TABLE streaming_history (
    stream_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
    track_id VARCHAR(50) REFERENCES tracks(track_id) ON DELETE CASCADE,
    played_at TIMESTAMP NOT NULL,
    ms_played INTEGER CHECK (ms_played > 0),
    
    -- Context information
    context_type VARCHAR(50),
    context_uri VARCHAR(255),
    context_name VARCHAR(255),
    
    -- Device and platform info
    platform VARCHAR(50),
    device_type VARCHAR(50),
    
    -- Session information
    session_id UUID,
    session_start TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Playlists for analysis
CREATE TABLE playlists (
    playlist_id VARCHAR(50) PRIMARY KEY,
    playlist_name VARCHAR(255) NOT NULL,
    user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    total_tracks INTEGER DEFAULT 0,
    spotify_uri VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Playlist tracks relationship
CREATE TABLE playlist_tracks (
    playlist_id VARCHAR(50) REFERENCES playlists(playlist_id) ON DELETE CASCADE,
    track_id VARCHAR(50) REFERENCES tracks(track_id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    position INTEGER,
    PRIMARY KEY (playlist_id, track_id)
);

-- =====================================================
-- ANALYTICS & DERIVED TABLES
-- =====================================================

-- Daily aggregated metrics for performance
CREATE TABLE daily_metrics (
    date DATE PRIMARY KEY,
    total_streams BIGINT DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    unique_tracks INTEGER DEFAULT 0,
    total_duration_minutes DECIMAL(10,2) DEFAULT 0,
    avg_session_duration_minutes DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Genre performance metrics (materialized view alternative)
CREATE TABLE genre_metrics (
    genre VARCHAR(100) PRIMARY KEY,
    total_tracks INTEGER DEFAULT 0,
    total_streams BIGINT DEFAULT 0,
    avg_popularity DECIMAL(5,2) DEFAULT 0,
    avg_danceability DECIMAL(5,3) DEFAULT 0,
    avg_energy DECIMAL(5,3) DEFAULT 0,
    avg_valence DECIMAL(5,3) DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Primary key indexes (automatically created)
-- Performance indexes for common queries
CREATE INDEX idx_tracks_artist_id ON tracks(artist_id);
CREATE INDEX idx_tracks_album_id ON tracks(album_id);
CREATE INDEX idx_tracks_popularity ON tracks(popularity);
CREATE INDEX idx_tracks_release_date ON tracks(release_date);
CREATE INDEX idx_tracks_genre ON tracks USING GIN(artist_id) WHERE artist_id IN (SELECT artist_id FROM artists WHERE genres IS NOT NULL);

CREATE INDEX idx_streaming_history_user_id ON streaming_history(user_id);
CREATE INDEX idx_streaming_history_track_id ON streaming_history(track_id);
CREATE INDEX idx_streaming_history_played_at ON streaming_history(played_at);
CREATE INDEX idx_streaming_history_session_id ON streaming_history(session_id);

CREATE INDEX idx_artists_popularity ON artists(popularity);
CREATE INDEX idx_artists_genres ON artists USING GIN(genres);

CREATE INDEX idx_albums_artist_id ON albums(artist_id);
CREATE INDEX idx_albums_release_date ON albums(release_date);

-- Composite indexes for complex queries
CREATE INDEX idx_tracks_artist_popularity ON tracks(artist_id, popularity);
CREATE INDEX idx_streaming_user_date ON streaming_history(user_id, played_at);
CREATE INDEX idx_tracks_features ON tracks(danceability, energy, valence, acousticness);

-- =====================================================
-- CONSTRAINTS & VALIDATIONS
-- =====================================================

-- Ensure valid audio feature ranges
ALTER TABLE tracks ADD CONSTRAINT chk_audio_features 
    CHECK (
        danceability >= 0.0 AND danceability <= 1.0 AND
        energy >= 0.0 AND energy <= 1.0 AND
        valence >= 0.0 AND valence <= 1.0 AND
        acousticness >= 0.0 AND acousticness <= 1.0 AND
        instrumentalness >= 0.0 AND instrumentalness <= 1.0 AND
        liveness >= 0.0 AND liveness <= 1.0 AND
        speechiness >= 0.0 AND speechiness <= 1.0
    );

-- Ensure valid musical attributes
ALTER TABLE tracks ADD CONSTRAINT chk_musical_attributes
    CHECK (
        key >= -1 AND key <= 11 AND
        mode IN (0, 1) AND
        time_signature >= 3 AND time_signature <= 7 AND
        tempo > 0
    );

-- =====================================================
-- TRIGGERS FOR DATA INTEGRITY
-- =====================================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers to relevant tables
CREATE TRIGGER update_artists_updated_at BEFORE UPDATE ON artists
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_albums_updated_at BEFORE UPDATE ON albums
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tracks_updated_at BEFORE UPDATE ON tracks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_playlists_updated_at BEFORE UPDATE ON playlists
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE artists IS 'Core artist information with popularity metrics and genre classifications';
COMMENT ON TABLE tracks IS 'Track metadata with comprehensive audio features for analysis';
COMMENT ON TABLE streaming_history IS 'User listening behavior with context and session information';
COMMENT ON TABLE daily_metrics IS 'Aggregated daily performance metrics for dashboard reporting';
COMMENT ON TABLE genre_metrics IS 'Pre-calculated genre performance metrics for fast analytics';

COMMENT ON COLUMN tracks.danceability IS 'How suitable a track is for dancing (0.0 = not danceable, 1.0 = very danceable)';
COMMENT ON COLUMN tracks.energy IS 'Perceptual measure of intensity and activity (0.0 = low energy, 1.0 = high energy)';
COMMENT ON COLUMN tracks.valence IS 'Musical positiveness (0.0 = negative, 1.0 = positive)';

-- =====================================================
-- SAMPLE DATA INSERTION (Optional)
-- =====================================================

-- Insert sample genres for testing
INSERT INTO genre_metrics (genre, total_tracks, total_streams, avg_popularity, avg_danceability, avg_energy, avg_valence) VALUES
('pop', 0, 0, 0.0, 0.0, 0.0, 0.0),
('rock', 0, 0, 0.0, 0.0, 0.0, 0.0),
('hip-hop', 0, 0, 0.0, 0.0, 0.0, 0.0),
('electronic', 0, 0, 0.0, 0.0, 0.0, 0.0),
('r&b', 0, 0, 0.0, 0.0, 0.0, 0.0)
ON CONFLICT (genre) DO NOTHING; 