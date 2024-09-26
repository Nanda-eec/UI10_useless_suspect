

#include "inspircd.h"

static bool MatchInternal(const unsigned char* str, const unsigned char* mask, const unsigned char* map)
{
	const unsigned char* cp = nullptr;
	const unsigned char* mp = nullptr;
	const unsigned char* string = reinterpret_cast<const unsigned char*>(str);
	const unsigned char* wild = reinterpret_cast<const unsigned char*>(mask);

	while ((*string) && (*wild != '*'))
	{
		if ((map[*wild] != map[*string]) && (*wild != '?'))
		{
			return false;
		}
		wild++;
		string++;
	}

	while (*string)
	{
		if (*wild == '*')
		{
			if (!*++wild)
			{
				return true;
			}
			mp = wild;
			cp = string+1;
		}
		else
			if ((map[*wild] == map[*string]) || (*wild == '?'))
			{
				wild++;
				string++;
			}
			else
			{
				wild = mp;
				string = cp++;
			}

	}

	while (*wild == '*')
	{
		wild++;
	}

	return !*wild;
}

// Below here is all wrappers around MatchInternal

bool InspIRCd::Match(const std::string& str, const std::string& mask, const unsigned char* map)
{
	if (!map)
		map = national_case_insensitive_map;

	return MatchInternal(reinterpret_cast<const unsigned char*>(str.c_str()), reinterpret_cast<const unsigned char*>(mask.c_str()), map);
}

bool InspIRCd::Match(const char* str, const char* mask, const unsigned char* map)
{
	if (!map)
		map = national_case_insensitive_map;

	return MatchInternal(reinterpret_cast<const unsigned char*>(str), reinterpret_cast<const unsigned char*>(mask), map);
}

bool InspIRCd::MatchCIDR(const std::string& str, const std::string& mask, const unsigned char* map)
{
	if (irc::sockets::MatchCIDR(str, mask, true))
		return true;

	// Fall back to regular match
	return InspIRCd::Match(str, mask, map);
}

bool InspIRCd::MatchCIDR(const char* str, const char* mask, const unsigned char* map)
{
	if (irc::sockets::MatchCIDR(str, mask, true))
		return true;

	// Fall back to regular match
	return InspIRCd::Match(str, mask, map);
}

bool InspIRCd::MatchMask(const std::string& masks, const std::string& hostname, const std::string& ipaddr)
{
	irc::spacesepstream masklist(masks);
	std::string mask;
	while (masklist.GetToken(mask))
	{
		if (InspIRCd::Match(hostname, mask, ascii_case_insensitive_map) ||
			InspIRCd::MatchCIDR(ipaddr, mask, ascii_case_insensitive_map))
		{
			return true;
		}
	}
	return false;
}
