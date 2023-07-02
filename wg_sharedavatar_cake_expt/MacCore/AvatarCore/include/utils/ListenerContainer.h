/********************************************************************
created:	2011/04/18
created:	18:4:2011   12:25
filename: 	d:\Development\mrayEngine\Engine\mrayEngine\include\ListenerContainer.h
file path:	d:\Development\mrayEngine\Engine\mrayEngine\include
file base:	ListenerContainer
file ext:	h
author:		MHD Yamen Saraiji

purpose:	
*********************************************************************/

#ifndef __ListenerContainer__
#define __ListenerContainer__

#include <list>

namespace utils
{

template <class T>
class ListenerContainer
{
public:
	typedef T ListenerType;

private:
protected:
	typedef std::list<T> ListenerList;
	ListenerList m_listeners;

public:
	ListenerContainer() {}
	virtual ~ListenerContainer()
	{
		ClearListeners();
	}

	void ClearListeners()
	{
		m_listeners.clear();
	}
	void AddListener(const ListenerType &l)
	{
        if(l)
            m_listeners.push_back(l);
	}
	void RemoveListener(const ListenerType &l)
	{
		auto it = m_listeners.begin();
		for (; it != m_listeners.end(); ++it)
		{
			if (*it == l)
			{
				m_listeners.erase(it);
				return;
			}
		}
	}

#define DECLARE_FIRE_METHOD(funcname, paramsDef, paramsCall) \
	void __FIRE_##funcname paramsDef                         \
	{                                                        \
		auto it = m_listeners.begin();                       \
		for (; it != m_listeners.end(); ++it)                \
		{                                                    \
			(*it)->funcname paramsCall;                      \
		}                                                    \
	}

#define FIRE_LISTENR_METHOD(funcname, paramsCall) \
	__FIRE_##funcname paramsCall;
};

} // namespace utils

#endif
