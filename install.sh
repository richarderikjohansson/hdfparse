#!/usr/bin/env bash

echo "Installing dependencies and CLI in .venv with uv"
uv sync

# Activate environment
VENV_DIR=".venv"
CURRENT_SHELL=$(basename "$SHELL")

case "$CURRENT_SHELL" in
  bash|zsh)
    if [ -f "$VENV_DIR/bin/activate" ]; then
      echo "Activating virtual environment for $CURRENT_SHELL..."
      source "$VENV_DIR/bin/activate"
    else
      echo "Activation script not found in $VENV_DIR/bin/activate"
      exit 1
    fi
    ;;
  fish)
    if [ -f "$VENV_DIR/bin/activate.fish" ]; then
      echo "Activating virtual environment for fish..."
      source "$VENV_DIR/bin/activate.fish"
    else
      echo "Activation script not found in $VENV_DIR/bin/activate.fish"
      exit 1
    fi
    ;;
  csh|tcsh)
    if [ -f "$VENV_DIR/bin/activate.csh" ]; then
      echo "Activating virtual environment for $CURRENT_SHELL..."
      source "$VENV_DIR/bin/activate.csh"
    else
      echo "Activation script not found in $VENV_DIR/bin/activate.csh"
      exit 1
    fi
    ;;
  *)
    echo "Unsupported shell: $CURRENT_SHELL"
    exit 1
    ;;
esac
