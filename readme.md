# Spotify Song Galaxy

An interactive data visualization of Spotify songs as an orbital galaxy, where each song is represented as an orb orbiting around a central point. The orbital speed and position are determined by the song's audio features.

## Features

- **Interactive Galaxy Visualization**: Songs displayed as glowing orbs orbiting in a galaxy-like formation
- **Tempo-Based Movement**: Orbital speed is directly proportional to the song's tempo (BPM)
  - High tempo songs orbit faster
  - Low tempo songs orbit slower
- **Mouse Hover Information**: Hover over any orb to see the track name, artist, and tempo
- **Zoom Controls**: 
  - Scroll mouse wheel to zoom in/out
  - Press `+` or `-` keys for precise zoom adjustment
- **Starry Background**: Beautiful space-themed background image
- **Data Sampling**: Loads up to 50 random songs from the dataset for optimal performance and visibility

## How It Works

### Visual Mapping
- **Orbital Radius**: Based on song danceability (more danceable = further from center)
- **Orb Size**: Based on song popularity (more popular = larger orb)
- **Orb Color**: Based on song valence/mood (sad/cold = blue, happy/warm = orange)
- **Glow Intensity**: Based on song energy (higher energy = brighter glow)

### Movement
- Each orb orbits the center point at a speed proportional to its BPM
- The visual formula: `speed = tempo * 0.002` (radians per second)

## Requirements

- Python 3.6+
- pygame
- A CSV file with Spotify song data (columns: `track_name`, `track_artist`, `tempo`, `danceability`, `energy`, `valence`, `track_popularity`)

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install pygame