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
#ifndef COMMANDMESSAGE_H
#define COMMANDMESSAGE_H

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

class DMBCommand final: public ::EmbeddedProto::MessageInterface
{
  public:
    DMBCommand() = default;
    DMBCommand(const DMBCommand& rhs )
    {
      set_command_enum(rhs.get_command_enum());
    }

    DMBCommand(const DMBCommand&& rhs ) noexcept
    {
      set_command_enum(rhs.get_command_enum());
    }

    ~DMBCommand() override = default;

    enum class Command : uint32_t
    {
      RSC_FIRST_INVALID = 0,
      RSC_ANY_TO_ABORT = 1,
      RSC_OPEN_VENT = 2,
      RSC_CLOSE_VENT = 3,
      RSC_OPEN_DRAIN = 4,
      RSC_CLOSE_DRAIN = 5,
      RSC_MEV_CLOSE = 6,
      RSC_GOTO_FILL = 7,
      RSC_ARM_CONFIRM_1 = 8,
      RSC_ARM_CONFIRM_2 = 9,
      RSC_GOTO_ARM = 10,
      RSC_GOTO_PRELAUNCH = 11,
      RSC_POWER_TRANSITION_ONBOARD = 12,
      RSC_POWER_TRANSITION_EXTERNAL = 13,
      RSC_GOTO_IGNITION = 14,
      RSC_IGNITION_TO_LAUNCH = 15,
      RSC_LAUNCH_TO_BURN = 16,
      RSC_BURN_TO_COAST = 17,
      RSC_COAST_TO_DESCENT = 18,
      RSC_DESCENT_TO_RECOVERY = 19,
      RSC_NONE = 20
    };

    enum class FieldNumber : uint32_t
    {
      NOT_SET = 0,
      COMMAND_ENUM = 1
    };

    DMBCommand& operator=(const DMBCommand& rhs)
    {
      set_command_enum(rhs.get_command_enum());
      return *this;
    }

    DMBCommand& operator=(const DMBCommand&& rhs) noexcept
    {
      set_command_enum(rhs.get_command_enum());
      return *this;
    }

    static constexpr char const* COMMAND_ENUM_NAME = "command_enum";
    inline void clear_command_enum() { command_enum_.clear(); }
    inline void set_command_enum(const Command& value) { command_enum_ = value; }
    inline void set_command_enum(const Command&& value) { command_enum_ = value; }
    inline const Command& get_command_enum() const { return command_enum_.get(); }
    inline Command command_enum() const { return command_enum_.get(); }


    ::EmbeddedProto::Error serialize(::EmbeddedProto::WriteBufferInterface& buffer) const override
    {
      ::EmbeddedProto::Error return_value = ::EmbeddedProto::Error::NO_ERRORS;

      if((static_cast<Command>(0) != command_enum_.get()) && (::EmbeddedProto::Error::NO_ERRORS == return_value))
      {
        return_value = command_enum_.serialize_with_id(static_cast<uint32_t>(FieldNumber::COMMAND_ENUM), buffer, false);
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
          case FieldNumber::COMMAND_ENUM:
            return_value = command_enum_.deserialize_check_type(buffer, wire_type);
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
      clear_command_enum();

    }

    static char const* field_number_to_name(const FieldNumber fieldNumber)
    {
      char const* name = nullptr;
      switch(fieldNumber)
      {
        case FieldNumber::COMMAND_ENUM:
          name = COMMAND_ENUM_NAME;
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

      left_chars = command_enum_.to_string(left_chars, indent_level + 2, COMMAND_ENUM_NAME, true);
  
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


      EmbeddedProto::enumeration<Command> command_enum_ = static_cast<Command>(0);

};

class PMBCommand final: public ::EmbeddedProto::MessageInterface
{
  public:
    PMBCommand() = default;
    PMBCommand(const PMBCommand& rhs )
    {
      set_command_enum(rhs.get_command_enum());
    }

    PMBCommand(const PMBCommand&& rhs ) noexcept
    {
      set_command_enum(rhs.get_command_enum());
    }

    ~PMBCommand() override = default;

    enum class Command : uint32_t
    {
      PMB_NONE = 0,
      PMB_OPEN_MEV = 1,
      PMB_CLOSE_MEV = 2,
      PMB_LAST = 3
    };

    enum class FieldNumber : uint32_t
    {
      NOT_SET = 0,
      COMMAND_ENUM = 1
    };

    PMBCommand& operator=(const PMBCommand& rhs)
    {
      set_command_enum(rhs.get_command_enum());
      return *this;
    }

    PMBCommand& operator=(const PMBCommand&& rhs) noexcept
    {
      set_command_enum(rhs.get_command_enum());
      return *this;
    }

    static constexpr char const* COMMAND_ENUM_NAME = "command_enum";
    inline void clear_command_enum() { command_enum_.clear(); }
    inline void set_command_enum(const Command& value) { command_enum_ = value; }
    inline void set_command_enum(const Command&& value) { command_enum_ = value; }
    inline const Command& get_command_enum() const { return command_enum_.get(); }
    inline Command command_enum() const { return command_enum_.get(); }


    ::EmbeddedProto::Error serialize(::EmbeddedProto::WriteBufferInterface& buffer) const override
    {
      ::EmbeddedProto::Error return_value = ::EmbeddedProto::Error::NO_ERRORS;

      if((static_cast<Command>(0) != command_enum_.get()) && (::EmbeddedProto::Error::NO_ERRORS == return_value))
      {
        return_value = command_enum_.serialize_with_id(static_cast<uint32_t>(FieldNumber::COMMAND_ENUM), buffer, false);
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
          case FieldNumber::COMMAND_ENUM:
            return_value = command_enum_.deserialize_check_type(buffer, wire_type);
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
      clear_command_enum();

    }

    static char const* field_number_to_name(const FieldNumber fieldNumber)
    {
      char const* name = nullptr;
      switch(fieldNumber)
      {
        case FieldNumber::COMMAND_ENUM:
          name = COMMAND_ENUM_NAME;
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

      left_chars = command_enum_.to_string(left_chars, indent_level + 2, COMMAND_ENUM_NAME, true);
  
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


      EmbeddedProto::enumeration<Command> command_enum_ = static_cast<Command>(0);

};

class CommandMessage final: public ::EmbeddedProto::MessageInterface
{
  public:
    CommandMessage() = default;
    CommandMessage(const CommandMessage& rhs )
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      set_source_sequence_num(rhs.get_source_sequence_num());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::DMB_COMMAND:
          set_dmb_command(rhs.get_dmb_command());
          break;

        case FieldNumber::PMB_COMMAND:
          set_pmb_command(rhs.get_pmb_command());
          break;

        default:
          break;
      }

    }

    CommandMessage(const CommandMessage&& rhs ) noexcept
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      set_source_sequence_num(rhs.get_source_sequence_num());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::DMB_COMMAND:
          set_dmb_command(rhs.get_dmb_command());
          break;

        case FieldNumber::PMB_COMMAND:
          set_pmb_command(rhs.get_pmb_command());
          break;

        default:
          break;
      }

    }

    ~CommandMessage() override = default;

    enum class FieldNumber : uint32_t
    {
      NOT_SET = 0,
      SOURCE = 1,
      TARGET = 2,
      MESSAGE_ID = 3,
      SOURCE_SEQUENCE_NUM = 4,
      DMB_COMMAND = 5,
      PMB_COMMAND = 6
    };

    CommandMessage& operator=(const CommandMessage& rhs)
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      set_source_sequence_num(rhs.get_source_sequence_num());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::DMB_COMMAND:
          set_dmb_command(rhs.get_dmb_command());
          break;

        case FieldNumber::PMB_COMMAND:
          set_pmb_command(rhs.get_pmb_command());
          break;

        default:
          break;
      }

      return *this;
    }

    CommandMessage& operator=(const CommandMessage&& rhs) noexcept
    {
      set_source(rhs.get_source());
      set_target(rhs.get_target());
      set_message_id(rhs.get_message_id());
      set_source_sequence_num(rhs.get_source_sequence_num());
      if(rhs.get_which_message() != which_message_)
      {
        // First delete the old object in the oneof.
        clear_message();
      }

      switch(rhs.get_which_message())
      {
        case FieldNumber::DMB_COMMAND:
          set_dmb_command(rhs.get_dmb_command());
          break;

        case FieldNumber::PMB_COMMAND:
          set_pmb_command(rhs.get_pmb_command());
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

    static constexpr char const* SOURCE_SEQUENCE_NUM_NAME = "source_sequence_num";
    inline void clear_source_sequence_num() { source_sequence_num_.clear(); }
    inline void set_source_sequence_num(const uint32_t& value) { source_sequence_num_ = value; }
    inline void set_source_sequence_num(const uint32_t&& value) { source_sequence_num_ = value; }
    inline uint32_t& mutable_source_sequence_num() { return source_sequence_num_.get(); }
    inline const uint32_t& get_source_sequence_num() const { return source_sequence_num_.get(); }
    inline uint32_t source_sequence_num() const { return source_sequence_num_.get(); }

    FieldNumber get_which_message() const { return which_message_; }

    static constexpr char const* DMB_COMMAND_NAME = "dmb_command";
    inline bool has_dmb_command() const
    {
      return FieldNumber::DMB_COMMAND == which_message_;
    }
    inline void clear_dmb_command()
    {
      if(FieldNumber::DMB_COMMAND == which_message_)
      {
        which_message_ = FieldNumber::NOT_SET;
        message_.dmb_command_.~DMBCommand();
      }
    }
    inline void set_dmb_command(const DMBCommand& value)
    {
      if(FieldNumber::DMB_COMMAND != which_message_)
      {
        init_message(FieldNumber::DMB_COMMAND);
      }
      message_.dmb_command_ = value;
    }
    inline void set_dmb_command(const DMBCommand&& value)
    {
      if(FieldNumber::DMB_COMMAND != which_message_)
      {
        init_message(FieldNumber::DMB_COMMAND);
      }
      message_.dmb_command_ = value;
    }
    inline DMBCommand& mutable_dmb_command()
    {
      if(FieldNumber::DMB_COMMAND != which_message_)
      {
        init_message(FieldNumber::DMB_COMMAND);
      }
      return message_.dmb_command_;
    }
    inline const DMBCommand& get_dmb_command() const { return message_.dmb_command_; }
    inline const DMBCommand& dmb_command() const { return message_.dmb_command_; }

    static constexpr char const* PMB_COMMAND_NAME = "pmb_command";
    inline bool has_pmb_command() const
    {
      return FieldNumber::PMB_COMMAND == which_message_;
    }
    inline void clear_pmb_command()
    {
      if(FieldNumber::PMB_COMMAND == which_message_)
      {
        which_message_ = FieldNumber::NOT_SET;
        message_.pmb_command_.~PMBCommand();
      }
    }
    inline void set_pmb_command(const PMBCommand& value)
    {
      if(FieldNumber::PMB_COMMAND != which_message_)
      {
        init_message(FieldNumber::PMB_COMMAND);
      }
      message_.pmb_command_ = value;
    }
    inline void set_pmb_command(const PMBCommand&& value)
    {
      if(FieldNumber::PMB_COMMAND != which_message_)
      {
        init_message(FieldNumber::PMB_COMMAND);
      }
      message_.pmb_command_ = value;
    }
    inline PMBCommand& mutable_pmb_command()
    {
      if(FieldNumber::PMB_COMMAND != which_message_)
      {
        init_message(FieldNumber::PMB_COMMAND);
      }
      return message_.pmb_command_;
    }
    inline const PMBCommand& get_pmb_command() const { return message_.pmb_command_; }
    inline const PMBCommand& pmb_command() const { return message_.pmb_command_; }


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

      if((0U != source_sequence_num_.get()) && (::EmbeddedProto::Error::NO_ERRORS == return_value))
      {
        return_value = source_sequence_num_.serialize_with_id(static_cast<uint32_t>(FieldNumber::SOURCE_SEQUENCE_NUM), buffer, false);
      }

      switch(which_message_)
      {
        case FieldNumber::DMB_COMMAND:
          if(has_dmb_command() && (::EmbeddedProto::Error::NO_ERRORS == return_value))
          {
            return_value = message_.dmb_command_.serialize_with_id(static_cast<uint32_t>(FieldNumber::DMB_COMMAND), buffer, true);
          }
          break;

        case FieldNumber::PMB_COMMAND:
          if(has_pmb_command() && (::EmbeddedProto::Error::NO_ERRORS == return_value))
          {
            return_value = message_.pmb_command_.serialize_with_id(static_cast<uint32_t>(FieldNumber::PMB_COMMAND), buffer, true);
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

          case FieldNumber::SOURCE_SEQUENCE_NUM:
            return_value = source_sequence_num_.deserialize_check_type(buffer, wire_type);
            break;

          case FieldNumber::DMB_COMMAND:
          case FieldNumber::PMB_COMMAND:
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
      clear_source_sequence_num();
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
        case FieldNumber::SOURCE_SEQUENCE_NUM:
          name = SOURCE_SEQUENCE_NUM_NAME;
          break;
        case FieldNumber::DMB_COMMAND:
          name = DMB_COMMAND_NAME;
          break;
        case FieldNumber::PMB_COMMAND:
          name = PMB_COMMAND_NAME;
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
      left_chars = source_sequence_num_.to_string(left_chars, indent_level + 2, SOURCE_SEQUENCE_NUM_NAME, false);
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
      EmbeddedProto::uint32 source_sequence_num_ = 0U;

      FieldNumber which_message_ = FieldNumber::NOT_SET;
      union message
      {
        message() {}
        ~message() {}
        DMBCommand dmb_command_;
        PMBCommand pmb_command_;
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
          case FieldNumber::DMB_COMMAND:
            new(&message_.dmb_command_) DMBCommand;
            break;

          case FieldNumber::PMB_COMMAND:
            new(&message_.pmb_command_) PMBCommand;
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
          case FieldNumber::DMB_COMMAND:
            ::EmbeddedProto::destroy_at(&message_.dmb_command_);
            break;
          case FieldNumber::PMB_COMMAND:
            ::EmbeddedProto::destroy_at(&message_.pmb_command_);
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
          case FieldNumber::DMB_COMMAND:
            return_value = message_.dmb_command_.deserialize_check_type(buffer, wire_type);
            break;
          case FieldNumber::PMB_COMMAND:
            return_value = message_.pmb_command_.deserialize_check_type(buffer, wire_type);
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
          case FieldNumber::DMB_COMMAND:
            left_chars = message_.dmb_command_.to_string(left_chars, indent_level, DMB_COMMAND_NAME, first_field);
            break;
          case FieldNumber::PMB_COMMAND:
            left_chars = message_.pmb_command_.to_string(left_chars, indent_level, PMB_COMMAND_NAME, first_field);
            break;
          default:
            break;
        }

        return left_chars;
      }

#endif // End of MSG_TO_STRING
};

} // End of namespace Proto
#endif // COMMANDMESSAGE_H