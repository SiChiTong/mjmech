// Copyright 2015 Josh Pieper, jjp@pobox.com.  All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include <boost/noncopyable.hpp>

#include <cstdint>
#include <string>

#include "fast_stream.h"
#include "telemetry_format.h"

namespace legtool {

/// Write log files with a format as described in telemetry_format.h.
class TelemetryLog : boost::noncopyable {
 public:
  class ThreadWriter;

  TelemetryLog();
  ~TelemetryLog();

  /// If true, then error if data is being written faster than it can
  /// be flushed to disk.  This must be called before any Open.
  void SetRealtime(bool);

  /// Open the given file for writing.
  void Open(const std::string& filename);

  /// Open a file descriptor for writing.
  void Open(int fd);

  /// Close the log, this is implicit at destruction time.
  void Close();

  /// Try to write all data to the operating system.  Note, this does
  /// not necessarily mean the data has been written to disk or a
  /// backing store.
  void Flush();

  /// Start a new log with the given file name.  All schema blocks
  /// written so far will be re-written to the start of this log.
  void Split(const std::string& name);

  /// Write a schema block to the log file.
  void WriteSchema(uint32_t identifier,
                   uint32_t block_schema_flags,
                   const std::string& record_name,
                   const std::string& schema);

  /// Write a data block to the log file.
  void WriteData(uint32_t identifier,
                 uint32_t block_data_flags,
                 const std::string& serialized_data);

  /// This raw API should only be used if you know what you are doing.
  /// It directly emits a block to the file store, and does not
  /// ensure that the block is properly formatted.
  void WriteBlock(TelemetryFormat::BlockType block_type,
                  const std::string& data);

  /// The following APIs are mimics which can be used to implement
  /// high-performance writing where no additional copies are
  /// necessary.

  class OStream : public FastOStringStream {
   private:
    OStream() {};

    void set_start(size_t start) { start_ = start; }
    size_t start() const { return start_; }

    void clear() {
      data()->clear();
      start_ = 0;
    }

    size_t start_ = 0;

    friend class ThreadWriter;
    friend class TelemetryLog;
  };

  /// Get a buffer which can be used to send data.
  std::unique_ptr<OStream> GetBuffer();

  // These variants of Write take a buffer, (which must have been
  // obtained by "GetBuffer" above), and returns ownership of the
  // buffer to the TelemetryLog class.

  void WriteData(uint32_t identifier,
                 uint32_t block_data_flags,
                 std::unique_ptr<OStream> buffer);
  void WriteBlock(TelemetryFormat::BlockType block_type,
                  std::unique_ptr<OStream> buffer);

 private:
  class Impl;
  std::unique_ptr<Impl> impl_;
};
}