/*
 *  Copyright (C) 2020-2023 Embedded AMS B.V. - All Rights Reserved
 *
 *  This file is part of Embedded Proto.
 *
 *  Embedded Proto is open source software: you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License as published
 *  by the Free Software Foundation, version 3 of the license.
 *
 *  Embedded Proto  is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Embedded Proto. If not, see <https://www.gnu.org/licenses/>.
 *
 *  For commercial and closed source application please visit:
 *  <https://EmbeddedProto.com/license/>.
 *
 *  Embedded AMS B.V.
 *  Info:
 *    info at EmbeddedProto dot com
 *
 *  Postal address:
 *    Johan Huizingalaan 763a
 *    1066 VH, Amsterdam
 *    the Netherlands
 */

// This file is generated. Please do not edit!
#ifndef TELEMETRYMESSAGE_H
#define TELEMETRYMESSAGE_H

#include <cstdint>
#include <MessageInterface.h>
#include <WireFormatter.h>
#include <Fields.h>
#include <MessageSizeCalculator.h>
#include <ReadBufferSection.h>
#include <RepeatedFieldFixedSize.h>
#include <FieldStringBytes.h>
#include <Errors.h>
#include <Defines.h>
#include <limits>

// Include external proto definitions
#include <CoreProto.h>

namespace Proto {

class TelemetryMessage final: public ::EmbeddedProto::MessageInterface
{
  public:
    TelemetryMessage() = default;
    TelemetryMessage(const TelemetryMessage& rhs )
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::PLACEHOLDER:
          set_placeholder(rhs.get_placeholder());
          break;

        default:
          break;
      }

    }

    TelemetryMessage(const TelemetryMessage&& rhs ) noexcept
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::PLACEHOLDER:
          set_placeholder(rhs.get_placeholder());
          break;

        default:
          break;
      }

    }

    ~TelemetryMessage() override = default;

    enum class FieldNumber : uint32_t
    {
      NOT_SET = 0,
      SOURCE = 1,
      TARGET = 2,
      MESSAGE_ID = 3,
      PLACEHOLDER = 4
    };

    TelemetryMessage& operator=(const TelemetryMessage& rhs)
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::PLACEHOLDER:
          set_placeholder(rhs.get_placeholder());
          break;

        default:
          break;
      }

      return *this;
    }

    TelemetryMessage& operator=(const TelemetryMessage&& rhs) noexcept
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::PLACEHOLDER:
          set_placeholder(rhs.get_placeholder());
          break;

        default:
          break;
      }

      return *this;
    }

    static constexpr char const* SOURCE_NAME = "source";
    inline void clear_source() { source_.clear(); }
    inline void set_source(const Node& value) { source_ = value; }
    inline void set_source(const Node&& value) { source_ = value; }
    inline const Node& get_source() const { return source_.get(); }
    inline Node source() const { return source_.get(); }

    static constexpr char const* TARGET_NAME = "target";
    inline void clear_target() { target_.clear(); }
    inline void set_target(const Node& value) { target_ = value; }
    inline void set_target(const Node&& value) { target_ = value; }
    inline const Node& get_target() const { return target_.get(); }
    inline Node target() const { return target_.get(); }

    static constexpr char const* MESSAGE_ID_NAME = "message_id";
    inline void clear_message_id() { message_id_.clear(); }
    inline void set_message_id(const uint32_t& value) { message_id_ = value; }
    inline void set_message_id(const uint32_t&& value) { message_id_ = value; }
    inline uint32_t& mutable_message_id() { return message_id_.get(); }
    inline const uint32_t& get_message_id() const { return message_id_.get(); }
    inline uint32_t message_id() const { return message_id_.get(); }

    FieldNumber get_which_message() const { return which_message_; }

    static constexpr char const* PLACEHOLDER_NAME = "placeholder";
    inline bool has_placeholder() const
    {
      return FieldNumber::PLACEHOLDER == which_message_;
    }
    inline void clear_placeholder()
    {
      if(FieldNumber::PLACEHOLDER == which_message_)
      {
        which_message_ = FieldNumber::NOT_SET;
        ::EmbeddedProto::destroy_at(&message_.placeholder_);
      }
    }
    inline void set_placeholder(const int32_t& value)
    {
      if(FieldNumber::PLACEHOLDER != which_message_)
      {
        init_message(FieldNumber::PLACEHOLDER);
      }
      message_.placeholder_ = value;
    }
    inline void set_placeholder(const int32_t&& value)
    {
      if(FieldNumber::PLACEHOLDER != which_message_)
      {
        init_message(FieldNumber::PLACEHOLDER);
      }
      message_.placeholder_ = value;
    }
    inline const int32_t& get_placeholder() const { return message_.placeholder_.get(); }
    inline int32_t placeholder() const { return message_.placeholder_.get(); }


    ::EmbeddedProto::Error serialize(::EmbeddedProto::WriteBufferInterface& buffer) const override
    {
      ::EmbeddedProto::Error return_value = ::EmbeddedProto::Error::NO_ERRORS;

      if((static_cast<Node>(0) != source_.get()) && (::EmbeddedProto::Error::NO_ERRORS == return_value))
      {
        return_value = source_.serialize_with_id(static_cast<uint32_t>(FieldNumber::SOURCE), buffer, false);
      }

      if((static_cast<Node>(0) != target_.get()) && (::EmbeddedProto::Error::NO_ERRORS == return_value))
      {
        return_value = target_.serialize_with_id(static_cast<uint32_t>(FieldNumber::TARGET), buffer, false);
      }

      if((0U != message_id_.get()) && (::EmbeddedProto::Error::NO_ERRORS == return_value))
      {
        return_value = message_id_.serialize_with_id(static_cast<uint32_t>(FieldNumber::MESSAGE_ID), buffer, false);
      }

      switch(which_message_)
      {
        case FieldNumber::PLACEHOLDER:
          if(has_placeholder() && (::EmbeddedProto::Error::NO_ERRORS == return_value))
          {
            return_value = message_.placeholder_.serialize_with_id(static_cast<uint32_t>(FieldNumber::PLACEHOLDER), buffer, true);
          }
          break;

        default:
          break;
      }

      return return_value;
    };

    ::EmbeddedProto::Error deserialize(::EmbeddedProto::ReadBufferInterface& buffer) override
    {
      ::EmbeddedProto::Error return_value = ::EmbeddedProto::Error::NO_ERRORS;
      ::EmbeddedProto::WireFormatter::WireType wire_type = ::EmbeddedProto::WireFormatter::WireType::VARINT;
      uint32_t id_number = 0;
      FieldNumber id_tag = FieldNumber::NOT_SET;

      ::EmbeddedProto::Error tag_value = ::EmbeddedProto::WireFormatter::DeserializeTag(buffer, wire_type, id_number);
      while((::EmbeddedProto::Error::NO_ERRORS == return_value) && (::EmbeddedProto::Error::NO_ERRORS == tag_value))
      {
        id_tag = static_cast<FieldNumber>(id_number);
        switch(id_tag)
        {
          case FieldNumber::SOURCE:
            return_value = source_.deserialize_check_type(buffer, wire_type);
            break;

          case FieldNumber::TARGET:
            return_value = target_.deserialize_check_type(buffer, wire_type);
            break;

          case FieldNumber::MESSAGE_ID:
            return_value = message_id_.deserialize_check_type(buffer, wire_type);
            break;

          case FieldNumber::PLACEHOLDER:
            return_value = deserialize_message(id_tag, buffer, wire_type);
            break;

          case FieldNumber::NOT_SET:
            return_value = ::EmbeddedProto::Error::INVALID_FIELD_ID;
            break;

          default:
            return_value = skip_unknown_field(buffer, wire_type);
            break;
        }

        if(::EmbeddedProto::Error::NO_ERRORS == return_value)
        {
          // Read the next tag.
          tag_value = ::EmbeddedProto::WireFormatter::DeserializeTag(buffer, wire_type, id_number);
        }
      }

      // When an error was detect while reading the tag but no other errors where found, set it in the return value.
      if((::EmbeddedProto::Error::NO_ERRORS == return_value)
         && (::EmbeddedProto::Error::NO_ERRORS != tag_value)
         && (::EmbeddedProto::Error::END_OF_BUFFER != tag_value)) // The end of the buffer is not an array in this case.
      {
        return_value = tag_value;
      }

      return return_value;
    };

    void clear() override
    {
      clear_source();
      clear_target();
      clear_message_id();
      clear_message();

    }

    static char const* field_number_to_name(const FieldNumber fieldNumber)
    {
      char const* name = nullptr;
      switch(fieldNumber)
      {
        case FieldNumber::SOURCE:
          name = SOURCE_NAME;
          break;
        case FieldNumber::TARGET:
          name = TARGET_NAME;
          break;
        case FieldNumber::MESSAGE_ID:
          name = MESSAGE_ID_NAME;
          break;
        case FieldNumber::PLACEHOLDER:
          name = PLACEHOLDER_NAME;
          break;
        default:
          name = "Invalid FieldNumber";
          break;
      }
      return name;
    }

#ifdef MSG_TO_STRING

    ::EmbeddedProto::string_view to_string(::EmbeddedProto::string_view& str) const
    {
      return this->to_string(str, 0, nullptr, true);
    }

    ::EmbeddedProto::string_view to_string(::EmbeddedProto::string_view& str, const uint32_t indent_level, char const* name, const bool first_field) const override
    {
      ::EmbeddedProto::string_view left_chars = str;
      int32_t n_chars_used = 0;

      if(!first_field)
      {
        // Add a comma behind the previous field.
        n_chars_used = snprintf(left_chars.data, left_chars.size, ",\n");
        if(0 < n_chars_used)
        {
          // Update the character pointer and characters left in the array.
          left_chars.data += n_chars_used;
          left_chars.size -= n_chars_used;
        }
      }

      if(nullptr != name)
      {
        if( 0 == indent_level)
        {
          n_chars_used = snprintf(left_chars.data, left_chars.size, "\"%s\": {\n", name);
        }
        else
        {
          n_chars_used = snprintf(left_chars.data, left_chars.size, "%*s\"%s\": {\n", indent_level, " ", name);
        }
      }
      else
      {
        if( 0 == indent_level)
        {
          n_chars_used = snprintf(left_chars.data, left_chars.size, "{\n");
        }
        else
        {
          n_chars_used = snprintf(left_chars.data, left_chars.size, "%*s{\n", indent_level, " ");
        }
      }
      
      if(0 < n_chars_used)
      {
        left_chars.data += n_chars_used;
        left_chars.size -= n_chars_used;
      }

      left_chars = source_.to_string(left_chars, indent_level + 2, SOURCE_NAME, true);
      left_chars = target_.to_string(left_chars, indent_level + 2, TARGET_NAME, false);
      left_chars = message_id_.to_string(left_chars, indent_level + 2, MESSAGE_ID_NAME, false);
      left_chars = to_string_message(left_chars, indent_level + 2, false);
  
      if( 0 == indent_level) 
      {
        n_chars_used = snprintf(left_chars.data, left_chars.size, "\n}");
      }
      else 
      {
        n_chars_used = snprintf(left_chars.data, left_chars.size, "\n%*s}", indent_level, " ");
      }

      if(0 < n_chars_used)
      {
        left_chars.data += n_chars_used;
        left_chars.size -= n_chars_used;
      }

      return left_chars;
    }

#endif // End of MSG_TO_STRING

  private:


      EmbeddedProto::enumeration<Node> source_ = static_cast<Node>(0);
      EmbeddedProto::enumeration<Node> target_ = static_cast<Node>(0);
      EmbeddedProto::uint32 message_id_ = 0U;

      FieldNumber which_message_ = FieldNumber::NOT_SET;
      union message
      {
        message() {}
        ~message() {}
        EmbeddedProto::int32 placeholder_;
      };
      message message_;

      void init_message(const FieldNumber field_id)
      {
        if(FieldNumber::NOT_SET != which_message_)
        {
          // First delete the old object in the oneof.
          clear_message();
        }

        // C++11 unions only support nontrivial members when you explicitly call the placement new statement.
        switch(field_id)
        {
          case FieldNumber::PLACEHOLDER:
            new(&message_.placeholder_) EmbeddedProto::int32;
            break;

          default:
            break;
         }

         which_message_ = field_id;
      }

      void clear_message()
      {
        switch(which_message_)
        {
          case FieldNumber::PLACEHOLDER:
            ::EmbeddedProto::destroy_at(&message_.placeholder_);
            break;
          default:
            break;
        }
        which_message_ = FieldNumber::NOT_SET;
      }

      ::EmbeddedProto::Error deserialize_message(const FieldNumber field_id, 
                                    ::EmbeddedProto::ReadBufferInterface& buffer,
                                    const ::EmbeddedProto::WireFormatter::WireType wire_type)
      {
        ::EmbeddedProto::Error return_value = ::EmbeddedProto::Error::NO_ERRORS;
        
        if(field_id != which_message_)
        {
          init_message(field_id);
        }

        switch(which_message_)
        {
          case FieldNumber::PLACEHOLDER:
            return_value = message_.placeholder_.deserialize_check_type(buffer, wire_type);
            break;
          default:
            break;
        }

        if(::EmbeddedProto::Error::NO_ERRORS != return_value)
        {
          clear_message();
        }
        return return_value;
      }

#ifdef MSG_TO_STRING 
      ::EmbeddedProto::string_view to_string_message(::EmbeddedProto::string_view& str, const uint32_t indent_level, const bool first_field) const
      {
        ::EmbeddedProto::string_view left_chars = str;

        switch(which_message_)
        {
          case FieldNumber::PLACEHOLDER:
            left_chars = message_.placeholder_.to_string(left_chars, indent_level, PLACEHOLDER_NAME, first_field);
            break;
          default:
            break;
        }

        return left_chars;
      }

#endif // End of MSG_TO_STRING
};

} // End of namespace Proto
#endif // TELEMETRYMESSAGE_H