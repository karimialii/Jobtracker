"""Theme configuration for the application."""
from dataclasses import dataclass
from enum import Enum


class Theme(Enum):
    """Available themes for the application."""
    LIGHT = "light"
    DARK = "dark"


@dataclass
class ThemeColors:
    """Color scheme for a theme."""
    bg: str
    fg: str
    button_bg: str
    button_fg: str
    entry_bg: str
    tree_bg: str
    tree_fg: str
    header_bg: str
    header_fg: str
    icon_bg: str


class ThemeConfig:
    """
    Theme configuration manager.
    
    Manages theme settings and provides theme switching functionality.
    """
    
    # Theme definitions - macOS style with proper contrast
    LIGHT_THEME = ThemeColors(
        bg="#FFFFFF",  # Clean white background
        fg="#000000",  # Pure black text
        button_bg="#007AFF",  # macOS blue
        button_fg="#FFFFFF",  # White text on blue
        entry_bg="#FFFFFF",  # White input fields
        tree_bg="#FFFFFF",  # White table background
        tree_fg="#000000",  # Black text for readability
        header_bg="#F5F5F7",  # Light gray header
        header_fg="#1D1D1F",  # Dark gray header text
        icon_bg="#F5F5F7"  # Match header
    )
    
    # Dark Mode with proper contrast
    DARK_THEME = ThemeColors(
        bg="#1C1C1E",  # Dark gray background
        fg="#FFFFFF",  # Pure white text
        button_bg="#0A84FF",  # Bright blue
        button_fg="#FFFFFF",  # White text
        entry_bg="#2C2C2E",  # Darker input fields
        tree_bg="#2C2C2E",  # Dark table background
        tree_fg="#FFFFFF",  # White text
        header_bg="#2C2C2E",  # Dark header
        header_fg="#FFFFFF",  # White header text
        icon_bg="#2C2C2E"  # Match header
    )
    
    # Status colors with better contrast
    STATUS_COLORS = {
        "applied": "#FFE066",  # Light yellow
        "rejected": "#FFB3B3",  # Light red
        "invited to interview": "#B3FFB3"  # Light green
    }
    
    # Visual properties
    VISUAL_PROPERTIES = {
        "corner_radius": 8,  # Subtle rounded corners
        "padding": 12,  # Standard padding
        "border_color": "#D1D1D6",  # Light border
        "border_width": 1,  # Thin border
    }
    
    # Icon paths
    ICON_PATHS = {
        Theme.LIGHT: "icons/light_icon.png",
        Theme.DARK: "icons/dark_icon.png"
    }
    
    def __init__(self):
        """Initialize theme configuration with default theme."""
        self._current_theme = Theme.LIGHT
    
    @property
    def current_theme(self) -> Theme:
        """Get the current theme."""
        return self._current_theme
    
    @current_theme.setter
    def current_theme(self, theme: Theme):
        """Set the current theme."""
        self._current_theme = theme
    
    def get_colors(self, theme: Theme = None) -> ThemeColors:
        """
        Get theme colors.
        
        Args:
            theme: Theme to get colors for (defaults to current theme)
            
        Returns:
            ThemeColors for the specified theme
        """
        theme = theme or self._current_theme
        return self.LIGHT_THEME if theme == Theme.LIGHT else self.DARK_THEME
    
    def get_icon_path(self, theme: Theme = None) -> str:
        """
        Get icon path for theme.
        
        Args:
            theme: Theme to get icon for (defaults to current theme)
            
        Returns:
            Path to theme icon
        """
        theme = theme or self._current_theme
        return self.ICON_PATHS[theme]
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self._current_theme = Theme.DARK if self._current_theme == Theme.LIGHT else Theme.LIGHT
    
    def get_status_color(self, status: str) -> str:
        """
        Get color for application status.
        
        Args:
            status: Application status
            
        Returns:
            Color code for the status
        """
        return self.STATUS_COLORS.get(status.lower(), "white")
    
    def get_ttk_theme(self) -> str:
        """
        Get ttk theme name based on current theme.
        
        Returns:
            ttk theme name
        """
        return "clam" if self._current_theme == Theme.DARK else "default"
