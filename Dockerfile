# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    git \
    cmake \
    curl \
    wget \
    libfftw3-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswresample-dev \
    libsamplerate0-dev \
    libtag1-dev \
    libchromaprint-dev \
    libyaml-dev \
    ffmpeg \
    libsndfile1 \
    libsndfile-dev \
    pkg-config \
    ninja-build \
    libeigen3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create Python symlink first
RUN ln -sf /usr/bin/python3 /usr/bin/python
# Upgrade pip and install specific numpy version
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install numpy==1.19.5

# Install TensorFlow C API and create necessary directories
RUN mkdir -p /tensorflow && \
    mkdir -p /usr/local/lib/pkgconfig && \
    cd /tensorflow && \
    wget https://storage.googleapis.com/tensorflow/libtensorflow/libtensorflow-cpu-linux-x86_64-2.6.0.tar.gz && \
    tar -C /usr/local -xzf libtensorflow-cpu-linux-x86_64-2.6.0.tar.gz && \
    ldconfig && \
    echo "/usr/local/lib" > /etc/ld.so.conf.d/tensorflow.conf && \
    ldconfig

# Set TensorFlow environment variables
ENV PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
ENV TENSORFLOW_ROOT=/usr/local

# Create pkgconfig file for TensorFlow
RUN printf "prefix=/usr/local\n\
exec_prefix=\${prefix}\n\
libdir=\${exec_prefix}/lib\n\
includedir=\${prefix}/include\n\
\n\
Name: tensorflow\n\
Version: 2.6.0\n\
Description: TensorFlow C library\n\
Libs: -L\${libdir} -ltensorflow\n\
Cflags: -I\${includedir}\n" > /usr/local/lib/pkgconfig/tensorflow.pc

# Install tensorflow and other Python dependencies
RUN python3 -m pip install \
    tensorflow==2.6.0 \
    six \
    pyyaml \
    wheel \
    setuptools

# Clone essentia
RUN git clone --branch master https://github.com/MTG/essentia.git

# Build essentia with tensorflow support
WORKDIR /essentia

# Get numpy include path
RUN python3 -c "import numpy; print(numpy.get_include())" > /tmp/numpy_include && \
    echo "Using NumPy include path: $(cat /tmp/numpy_include)"

# Set compiler flags including numpy include path
ENV CXXFLAGS="-DEIGEN_MAX_ALIGN_BYTES=16 -DEIGEN_DONT_VECTORIZE -I$(cat /tmp/numpy_include)"
ENV CPPFLAGS="-I$(cat /tmp/numpy_include)"

# Configure and build
RUN python3 waf configure --build-static --with-tensorflow --with-python && \
    python3 waf && \
    python3 waf install && \
    ldconfig

# Set working directory for our app
WORKDIR /app

# Copy requirements first
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Create directories
RUN mkdir -p /app/uploads /app/analysis_files /app/templates /app/static /app/essentia_graphfiles

# Copy application files
COPY templates/ /app/templates/
COPY static/ /app/static/
COPY *.py /app/
COPY models/ /app/models/
COPY essentia_graphfiles/ /app/essentia_graphfiles/

# Set permissions
RUN chmod -R 755 /app

# Verify installation
RUN python3 -c "from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs; print('Essentia with TensorFlow OK')"

EXPOSE 8080

CMD ["python3", "-u", "app.py"]